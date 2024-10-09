# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline

# # Load the pre-trained NER model and tokenizer
# model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
# tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

# # Create a pipeline for named entity recognition
# ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# # Example text (your provided input)
# text = """
# The GE414 engine is a powerful and reliable system that powers the F18 aircraft, requiring regular maintenance to ensure optimal performance. Basic maintenance tasks include inspecting and cleaning the air intake, verifying the condition of the compressor blades, and checking for signs of wear or damage in the turbine section. During each maintenance cycle, it is essential to clean the filters and lubricate moving parts to prevent mechanical failures."""

# # Apply the NER pipeline to extract named entities
# entities = ner_pipeline(text)

# # Print the extracted entities
# for entity in entities:
#     print(f"Entity: {entity['word']}, Label: {entity['entity_group']}")


from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import torch

# Load the pre-trained NER model and tokenizer
model = AutoModelForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

# Check if GPU is available, otherwise fall back to CPU
device = 0 if torch.cuda.is_available() else -1

# Create a pipeline for named entity recognition, using GPU if available
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)

# Example text (your provided input)
text = """
The M551 Sheridan light tank, known for its mobility and versatility, is equipped with a diesel engine that relies heavily on a well-maintained  GE87 air intake system for optimal performance. Proper upkeep of the air intake filter is critical to ensure the engine receives clean, debris-free air, which helps maintain efficient combustion and prevents engine wear."""

# Apply the NER pipeline to extract named entities
entities = ner_pipeline(text)

# Print the extracted entities
for entity in entities:
    print(f"Entity: {entity['word']}, Label: {entity['entity_group']}")
