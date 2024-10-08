import logging

logging.basicConfig(
    filename='/Users/livinginexile/Documents/Discogs Python/Sales Monitor/test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("Test cron job ran successfully")