import json
import re
import os

def load_data(file_path):
    """
    Load the raw JSON data from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def clean_text(text):
    """
    Clean the text by removing unwanted characters and normalizing spaces.
    """
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^\w\s።፥፡፣፤፦፨]', '', text)  # Remove punctuation except Amharic-specific ones
    return text.strip()

def tokenize_message(message):
    """
    Tokenize the cleaned message by splitting based on spaces.
    """
    tokens = message.split(' ')
    return tokens

def preprocess_data(messages):
    """
    Apply cleaning and tokenization to each message in the dataset.
    """
    for message in messages:
        if message['message']:
            message['clean_message'] = clean_text(message['message'])
            message['tokens'] = tokenize_message(message['clean_message'])
    return messages

def save_preprocessed_data(messages, filename):
    """
    Save the preprocessed messages to a JSON file.
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    
    raw_data_path = 'data/raw/@sinayelj_messages.json'
    messages = load_data(raw_data_path)

    # Preprocess the data
    processed_messages = preprocess_data(messages)

    # Save the preprocessed data
    save_preprocessed_data(processed_messages, 'data/processed/processed_messages.json')
    print("Preprocessing completed and data saved to data/processed/processed_messages.json")
