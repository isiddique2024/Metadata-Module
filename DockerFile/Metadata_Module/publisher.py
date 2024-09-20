import socket
import bson  # Binary JSON format
import threading  # For handling multiple clients concurrently
import pika  # RabbitMQ client library
from pika.exchange_type import ExchangeType
from copy import deepcopy  # Import deepcopy if you need a deep copy

def recvall(sock, expected_length):
    data = b''
    while len(data) < expected_length:
        more_data = sock.recv(expected_length - len(data))
        if not more_data:
            raise Exception("Socket closed before we received the complete document")
        data += more_data
    return data

def handle_client(client):
    # Initially, receive the length of the BSON document (first 4 bytes)
    length_data = client.recv(4)
    if len(length_data) < 4:
        print("Failed to receive the complete length of BSON document")
        return

    # Determine the expected length of the BSON document
    expected_length = int.from_bytes(length_data, byteorder='little')
    
    # Receive the rest of the BSON document based on its length
    bson_data = length_data + recvall(client, expected_length - 4)

    try:
        obj = bson.loads(bson_data)
        publish_to_rabbitmq('.Status.', obj)
    except Exception as e:
        print(f"Error decoding BSON: {e}")
   

# Function to publish messages to RabbitMQ
def publish_to_rabbitmq(routing_key, message):
    try:
        # Establish a connection to the RabbitMQ server
        connection_parameters = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(connection_parameters)

        # Create a channel for communication with RabbitMQ
        channel = connection.channel()

        #prepping status message
        status_message = message.copy()
 

        
        status_message=bson.dumps(status_message)

        # Serialize the message to BSON
        message = bson.dumps(message)

        '''
        This will be sent to the dashboard
         {
         
         'JobID': '0.3864155992230227', 
         'contentID': '123456', 
         'Status': 'user inout for now', 
         'timestamp': '2024-09-19 16:57:05', 
         'details': 1,
        }
        '''
        #publish status message to dashboard
        channel.basic_publish(
            exchange="Topic",
            routing_key=".Status.",
            body=status_message
        )

    except Exception as e:
        '''
        This will be sent to the dashboard
            {
                "ID": "ObjectID",  
                "DocumentId": "ObjectID",
                "DocumentType": "String",
                "FileName": "String",
                "Status": "Preprocessing Failed",
                "Message": "String"
            }
        '''
        status_message = message.copy()
        del status_message['Payload']
        status_message['Status'] = 'Preprocessing Failed'
        status_message['Message'] = e
        status_message=bson.dumps(status_message)
        channel.basic_publish(
            exchange="Topic",
            routing_key=".Status.",
            body= status_message
        )
    # Close the connection to RabbitMQ
    connection.close()

# Function to start a socket server and listen for incoming BSON objects
def receive_bson_obj():
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to localhost on port 12345
        s.bind(('localhost', 12345))
        # Listen for incoming connections
        s.listen()

        # Continuously accept new connections
        while True:
            # Accept a connection
            conn, addr = s.accept()
            print('Connected by', addr)
            # Handle each client connection in a separate thread
            threading.Thread(target=handle_client, args=(conn,)).start()
    

# Main function to start the server
if __name__ == '__main__':
    receive_bson_obj()
    print("all message send")
