import spacy

nlp = spacy.blank("en")
doc = nlp("The M551 Sheridan light tank, known for its mobility and versatility, is equipped with a diesel engine that relies heavily on a well-maintained  GE87 air intake system for optimal performance.")

# Print each token and its position in the text
for token in doc:
    print(f"Token: {token.text}, Start: {token.idx}, End: {token.idx + len(token)}")
