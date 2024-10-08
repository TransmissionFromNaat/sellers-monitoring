import json
import os

DATA_FILE = '/Users/livinginexile/Documents/Discogs Python/Sales Monitor/sellers_data.json'

def load_previous_sellers():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return {release_id: set(sellers) for release_id, sellers in data.items()}
    else:
        return {}

def save_current_sellers(sellers_data):
    data = {release_id: list(sellers) for release_id, sellers in sellers_data.items()}
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)