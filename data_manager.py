import json
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sellers_data.json')

def load_previous_sellers():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                content = file.read().strip()
                if not content:
                    logging.warning(f"{DATA_FILE} is empty. Starting with empty data.")
                    return {}
                data = json.loads(content)
                previous_sellers = {release_id: set(sellers) for release_id, sellers in data.items()}
                logging.debug(f"Loaded previous_sellers: {previous_sellers}")
                return previous_sellers
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {DATA_FILE}: {e}")
            return {}
        except Exception as e:
            logging.error(f"Error loading previous sellers from {DATA_FILE}: {e}")
            return {}
    else:
        logging.warning(f"{DATA_FILE} not found. Starting with empty data.")
        return {}

def save_current_sellers(sellers_data):
    data = {release_id: list(sellers) for release_id, sellers in sellers_data.items()}
    logging.debug(f"Data to be saved: {data}")
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)
        logging.debug(f"Successfully saved data to {DATA_FILE}")
    except Exception as e:
        logging.error(f"Error saving current sellers to {DATA_FILE}: {e}")
        raise