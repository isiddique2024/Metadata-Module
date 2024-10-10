import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding

# Create a blank English model
nlp = spacy.blank("en")

# Create the NER component
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Updated training data with corrected offsets
TRAIN_DATA = [
    ("The GE414 engine powers the F18 aircraft.", {"entities": [(4, 9, "ENGINE"), (28, 31, "AIRCRAFT")]}),
  
]

# Add labels to the NER component
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Disable other pipes for training
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

# Start the training
with nlp.disable_pipes(*unaffected_pipes):
    optimizer = nlp.begin_training()
    for iteration in range(30):  # 30 iterations, adjust if needed
        losses = {}
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            examples = []
            for text, annotations in batch:
                # Create a Doc object and Example object
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                examples.append(example)

            # Update the model with the Example objects
            nlp.update(examples, drop=0.5, losses=losses)

        print(f"Iteration {iteration + 1} Losses: {losses}")

# Save the trained model
nlp.to_disk("./custom_ner_model")
