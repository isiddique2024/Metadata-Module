import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer, DataCollatorForTokenClassification
from datasets import DatasetDict, Dataset

# Step 1: Define label to ID mapping
label_list = ["O", "B-ENGINE", "I-ENGINE"]  # Add all unique labels in your dataset
label_to_id = {label: i for i, label in enumerate(label_list)}

# Step 2: Load and Parse the Text File
def load_text_file(file_path):
    tokens = []
    ner_tags = []
    token_sentence = []
    tag_sentence = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() == "":  # End of a sentence
                if token_sentence and tag_sentence:
                    tokens.append(token_sentence)
                    ner_tags.append([label_to_id[tag] for tag in tag_sentence])  # Convert tags to IDs
                token_sentence = []
                tag_sentence = []
            else:
                token, tag = line.strip().split()
                token_sentence.append(token)
                tag_sentence.append(tag)

        # To capture the last sentence
        if token_sentence and tag_sentence:
            tokens.append(token_sentence)
            ner_tags.append([label_to_id[tag] for tag in tag_sentence])

    return tokens, ner_tags

# Load your text data
file_path = "bertNerTrainData.txt"  # Update with the correct file path
tokens, ner_tags = load_text_file(file_path)

# Step 3: Convert to Dataset Format
dataset_dict = {
    'train': {
        'tokens': tokens,
        'ner_tags': ner_tags
    }
}

# Create a DatasetDict and Dataset
dataset = DatasetDict({
    'train': Dataset.from_dict(dataset_dict['train'])
})

# Step 4: Load Pre-trained BERT Model and Tokenizer
model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Step 5: Tokenize the Dataset and Align Labels
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples['tokens'], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples['ner_tags']):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their original word
        label_ids = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # Ignore special tokens
            elif word_idx != previous_word_idx:  # Label for the first token of each word
                label_ids.append(label[word_idx])
            else:  # Use -100 for subsequent wordpieces of the same word
                label_ids.append(-100)
            previous_word_idx = word_idx
        tokenized_inputs['labels'] = label_ids
    return tokenized_inputs

tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=True)

# Step 6: Set up Training Arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Step 7: Data Collator
data_collator = DataCollatorForTokenClassification(tokenizer)

# Step 8: Trainer Instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Step 9: Train the Model
trainer.train()

# Step 10: Save the Fine-tuned Model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

print("Model fine-tuning complete and saved.")
