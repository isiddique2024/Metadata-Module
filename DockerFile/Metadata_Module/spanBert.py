from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import torch

# Load the pre-trained SpanBERT model and tokenizer
model = AutoModelForTokenClassification.from_pretrained("./results")
tokenizer = AutoTokenizer.from_pretrained("./results")

# Check if GPU is available, otherwise fall back to CPU
device = 0 if torch.cuda.is_available() else -1

# Create a pipeline for named entity recognition, using GPU if available
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)

# Example text (your provided input)
text = """
The M551 Sheridan light tank, known for its mobility and versatility, is equipped with a diesel engine that relies heavily on a well-maintained GE87 air intake system for optimal performance. Proper upkeep of the air intake filter is critical to ensure the engine receives clean, debris-free air, which helps maintain efficient combustion and prevents engine wear.
"""

# Apply the NER pipeline to extract named entities
entities = ner_pipeline(text)

# Print the extracted entities
for entity in entities:
    print(f"Entity: {entity['word']}, Label: {entity['entity_group']}")
