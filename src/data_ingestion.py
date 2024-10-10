from telethon import TelegramClient, sync
import json
import os

# Replace these with your own credentials
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')

# The session name (can be any string you choose)
session_name = 'telegram_data_ingestion'

# Create the Telegram client
client = TelegramClient(session_name, api_id, api_hash)
client.start()

# Specify the Telegram channel you want to scrape data from
channel = '@sinayelj'

# Function to fetch messages from a channel
def fetch_messages(channel, limit=100):
    messages = []
    for message in client.iter_messages(channel, limit=limit):
        # Prepare a dictionary to store the message data
        message_data = {
            'id': message.id,
            'sender_id': message.sender_id,
            'message': message.message,
            'date': str(message.date),
            'media': None
        }
        
        # Check if the message contains media
        if message.media:
            if isinstance(message.media, type(message.photo)):  # Check if it's a photo
                message_data['media'] = 'photo'
            else:
                message_data['media'] = 'other'

        messages.append(message_data)
    return messages

# Function to save messages to a JSON file
def save_messages(messages, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print(f"Fetching messages from {channel}...")
    messages = fetch_messages(channel)
    save_messages(messages, f'data/raw/{channel}_messages.json')
    print(f"Saved messages to data/raw/{channel}_messages.json")

# Disconnect the client after fetching data
client.disconnect()
