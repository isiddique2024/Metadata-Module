import spacy

# Load a blank English model
nlp = spacy.blank("en")

# Get sentence input from the user
sentence = input("Please enter a sentence: ")
doc = nlp(sentence)

# Initialize an empty list to store entities
entities = []

while True:
    # Print each token and its position in the text
    print("\nTokens:")
    for token in doc:
        print(f"Token: {token.text}, Start: {token.idx}, End: {token.idx + len(token)}")

    # Ask the user which phrase they want to index
    phrase_to_index = input("Which phrase would you like to index? (Type the phrase or 'done' to finish): ")

    if phrase_to_index.lower() == 'done':
        break

    # Split the phrase into tokens and find the start and end indices
    phrase_tokens = phrase_to_index.split()
    
    # Initialize variables to store the start and end indices
    start_index = None
    end_index = None
    entity_label = None
    
    for token in doc:
        if token.text in phrase_tokens:
            # Determine the start index
            if start_index is None:
                start_index = token.idx
            # Update end_index to the last matching token
            end_index = token.idx + len(token)

    # If both start_index and end_index are found
    if start_index is not None and end_index is not None:
        # Ask for the entity label
        entity_label = input("Please enter the entity label (e.g., 'digitalTwinElectricGenerator'): ")
        entities.append((start_index, end_index, entity_label))
    else:
        print("Phrase not found. Please try again.")

# Create the output format
output = (sentence, {"entities": entities})
print("\nOutput:")
print(output)
