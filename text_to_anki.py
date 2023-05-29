import requests
import csv

DECK_NAME = "Testing"

def write_to_anki(card_list):
    # Set the URL for the AnkiConnect API
    url = "http://localhost:8765"

    # Set the deck name you want to add the cards to

    for card in card_list:
        # Construct the JSON payload for the AnkiConnect API request
        front = card[0]
        back = card[1]
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": DECK_NAME,
                    "modelName": "Basic",
                    "fields": {
                        "Front": front,
                        "Back": back
                    },
                    "options": {
                        "allowDuplicate": False
                    },
                    "tags": []
                }
            }
        }
        
        # Make the AnkiConnect API request
        response = requests.post(url, json=payload)

        # Check if the response was successful
        if response.status_code != 200:
            print(f"Failed to add card: {front} -> {back}")
        else:
            print(f"Added card: {front} -> {back}")