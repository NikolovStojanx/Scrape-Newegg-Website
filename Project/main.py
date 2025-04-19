import json
import threading
from db.postgres_handler import PostgresHandler
from scraper.newegg_scraper import NeweggScraper
from utils.config import DB_CONFIG, MAX_PRODUCTS

def scrape_category(db_handler, scraper, url):
    scraper.scrape_paginated(db_handler, url)

def main():
    db_handler = PostgresHandler(**DB_CONFIG)
    scraper = NeweggScraper(max_products=MAX_PRODUCTS)
    threads = []

    with open("./data/categories_links.json", "r") as f:
        categories = json.load(f)

    try:
        for url in categories:
            thread = threading.Thread(target=scrape_category, args=(db_handler, scraper, url))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    finally:
        db_handler.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()