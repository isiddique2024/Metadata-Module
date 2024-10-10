import spacy

# Load your custom-trained model
nlp_custom = spacy.load("./custom_ner_model")

# Test on some sample text
doc = nlp_custom("The GE534 engine powers the F18 aircraft.")
for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")
