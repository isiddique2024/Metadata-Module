from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Define a function to read the text file and return tokens and labels
def read_txt_dataset(filepath):
    tokens, labels = [], []
    current_tokens, current_labels = [], []
    
    with open(filepath, "r") as file:
        for line in file:
            if line.strip() == "":  # Empty line indicates sentence boundary
                if current_tokens:
                    tokens.append(current_tokens)
                    labels.append(current_labels)
                    current_tokens, current_labels = [], []
            else:
                token, label = line.strip().split()  # Assuming "Token Label" format
                current_tokens.append(token)
                current_labels.append(label)
        
        # Add last sentence
        if current_tokens:
            tokens.append(current_tokens)
            labels.append(current_labels)
    
    return tokens, labels

# Load the dataset
tokens, labels = read_txt_dataset("bertNerTrainData.txt")

# Convert the dataset into a Hugging Face Dataset object
dataset_dict = {"tokens": tokens, "labels": labels}
dataset = Dataset.from_dict(dataset_dict)

# Define label mapping
label_list = list(set([label for sublist in labels for label in sublist]))
label_map = {label: idx for idx, label in enumerate(label_list)}

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained("SpanBERT/spanbert-base-cased")

# Tokenize and encode the dataset
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True, padding=True)
    
    labels = []
    for i, label in enumerate(examples["labels"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # Special tokens
            elif word_idx != previous_word_idx:
                label_ids.append(label_map[label[word_idx]])
            else:
                label_ids.append(-100)  # For subwords
            previous_word_idx = word_idx
        labels.append(label_ids)
    
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Apply the tokenization and alignment function
tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)

# Load the SpanBERT model for token classification
model = AutoModelForTokenClassification.from_pretrained("SpanBERT/spanbert-base-cased", num_labels=len(label_list))

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Define the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,  # Replace with validation data if available
)

# Train the model
trainer.train()
# After training, save the model and tokenizer
trainer.save_model("./results")  # Save the model and tokenizer
tokenizer.save_pretrained("./results")

