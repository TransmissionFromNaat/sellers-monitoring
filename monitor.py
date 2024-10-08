import cloudscraper
import os
import logging
from bs4 import BeautifulSoup
from email_notifications import send_email_notification
from data_manager import load_previous_sellers, save_current_sellers

logging.basicConfig(
    filename='/Users/livinginexile/Documents/Discogs Python/Sales Monitor/script.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Cron Environment Variables:")
for key, value in os.environ.items():
    logging.info(f"{key}: {value}")

logging.info("Script starts")

def get_release_title(soup):
    """Extract the title of the release from the page."""
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.text.replace(" | Discogs", "").strip()
    return "Unknown Title"

def get_current_sellers(release_id):
    url = f'https://www.discogs.com/sell/release/{release_id}?ev=rb'
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    sellers = set()
    table = soup.find('table', class_='table_block')
    
    if table:
        rows = table.find('tbody').find_all('tr')
        logging.info(f"Found {len(rows)} seller rows for release ID {release_id}")
        for row in rows:
            seller_info = row.find('td', class_='seller_info')
            if seller_info:
                seller_name_tag = seller_info.find('a')
                if seller_name_tag:
                    seller_name = seller_name_tag.text.strip().lower()
                    logging.info(f"Extracted seller name: '{seller_name}'")
                    sellers.add(seller_name)
            else:
                logging.warning(f"Seller info not found in row for release ID {release_id}")
    else:
        logging.warning(f"Table not found for release ID {release_id}")

    
    release_title = get_release_title(soup)
    logging.info(f"Release Title: {release_title}")

    logging.info(f"Extracted {len(sellers)} sellers for release ID {release_id}: {sellers}")
    return release_title, sellers

def monitor_individual_releases(release_ids):
    logging.info("Script starts")
    previous_sellers = load_previous_sellers()
    current_sellers = {}

    for release_id in release_ids:
        logging.info(f"Checking release ID: {release_id}")
        try:
            release_title, sellers = get_current_sellers(release_id)
            current_sellers[release_id] = sellers

            if release_id in previous_sellers:
                new_sellers = sellers - previous_sellers.get(release_id, set())
                logging.info(f"Previous sellers for release ID {release_id}: {previous_sellers.get(release_id, set())}")
                logging.info(f"Current sellers for release ID {release_id}: {sellers}")

                if new_sellers:
                    logging.info(f"New sellers found for release ID {release_id}: {new_sellers}")
                    send_email_notification(release_id, release_title, new_sellers)
                else:
                    logging.info(f"No new sellers for release ID {release_id}")
            else:
                logging.info(f"New release ID {release_id} added to tracking, no email notification sent.")
            
            previous_sellers[release_id] = sellers

        except Exception as e:
            logging.error(f"Error checking release ID {release_id}: {e}")

    save_current_sellers(current_sellers)
    logging.info("Script ends")