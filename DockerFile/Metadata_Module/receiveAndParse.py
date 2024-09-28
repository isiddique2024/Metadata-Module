import pika
import bson
import os
import logging
from threading import Event

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Disable pika's DEBUG logging
logging.getLogger("pika").setLevel(logging.WARNING)

# Global variable to store the current document's content ID
current_content_id = None
current_folder = None


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
    return directory


def save_file(file_path, data):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(data)
        logging.info(f"File saved successfully: {file_path}")
        logging.debug(f"File size: {len(data)} bytes")
    except Exception as e:
        logging.error(f"Error saving file {file_path}: {str(e)}")


def process_document(channel, method, properties, body):
    global current_content_id, current_folder
    try:
        obj = bson.loads(body)
        content_id = obj["ContentId"]
        file_name = obj["FileName"]

        current_content_id = content_id
        current_folder = f"{content_id}+{file_name}"
        base_path = create_dir(current_folder)

        document_file_name = f"{file_name}+{content_id}"
        save_file(os.path.join(base_path, document_file_name), obj["Payload"])

        logging.info(f"Processed document with content ID: {content_id}")
        channel.basic_ack(delivery_tag=method.delivery_tag)

        # Now process related images
        process_related_images(channel)

    except KeyError as e:
        logging.error(f"Missing key in document message: {str(e)}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except bson.errors.BSONError:
        logging.error("Failed to decode BSON message for document")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        logging.error(f"Error processing document message: {str(e)}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def process_image(channel, method, properties, body):
    try:
        obj = bson.loads(body)
        content_id = obj["ContentId"]
        file_name = obj["FileName"]

        if content_id != current_content_id:
            logging.info(f"Skipping image with non-matching content ID: {content_id}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            return False

        image_file_name = f"image_{file_name}+{content_id}"
        save_file(os.path.join(current_folder, image_file_name), obj["Payload"])

        logging.info(f"Processed image with content ID: {content_id}")
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return True

    except KeyError as e:
        logging.error(f"Missing key in image message: {str(e)}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except bson.errors.BSONError:
        logging.error("Failed to decode BSON message for image")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        logging.error(f"Error processing image message: {str(e)}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    return False


def process_related_images(channel):
    image_queue_name = "Image"
    while True:
        method_frame, header_frame, body = channel.basic_get(queue=image_queue_name)
        if method_frame:
            if process_image(channel, method_frame, header_frame, body):
                continue
            else:
                break
        else:
            logging.info("No more images to process for the current document")
            break


def start_receiver():
    connection_params = pika.ConnectionParameters(
        "localhost", heartbeat=600, blocked_connection_timeout=300
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    exchange_name = "Topic"
    channel.exchange_declare(
        exchange=exchange_name, exchange_type="topic", durable=True
    )

    document_queue_name = "Document"
    image_queue_name = "Image"

    channel.queue_declare(queue=document_queue_name, durable=True, arguments=None)
    channel.queue_declare(queue=image_queue_name, durable=True, arguments=None)

    channel.queue_bind(
        exchange=exchange_name, queue=document_queue_name, routing_key="*.Document.*"
    )
    channel.queue_bind(
        exchange=exchange_name, queue=image_queue_name, routing_key="*.Image.*"
    )

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=document_queue_name, on_message_callback=process_document
    )

    logging.info("Waiting for documents...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Interrupted by user, shutting down...")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    start_receiver()
