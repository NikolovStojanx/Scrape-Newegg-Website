import re
import threading
import time
from Project import url_to_soup



class NeweggScraper:

    def __init__(self, max_products=50):
        self.max_products = max_products
        self.product_count = 0
        self.lock = threading.Lock()

    def get_rating_second_structure(self, soup):
        try:
            rating = float(soup.find('div', class_='product-reviews').find('i')['title'].split(' ')[0])
            reviews_count = int(
                soup.find('div', class_='product-reviews').find('span', class_='item-rating-num').text.split(' ')[
                    0].replace('(', ''))
        except:
            return [None, None]

        return [rating, reviews_count]

    def scrape_page(self, url):
        soup = url_to_soup.get_soup_from_url(url)
        products_data = []

        for item_cell in soup.find_all('div', class_='item-cell'):
            try:
                title_element = item_cell.find('a', class_='item-title')
                product_title = title_element.text.strip() if title_element else None

                price_strong = item_cell.find('li', class_='price-current').find('strong')
                price_sup = item_cell.find('li', class_='price-current').find('sup')
                price_text = f"{price_strong.text.strip()}{price_sup.text.strip()}" if price_strong and price_sup else None
                final_price = float(re.sub(r'[^\d.]', '', price_text)) if price_text else None

                brand_element = item_cell.find('a', class_='item-brand')
                seller = brand_element.find('img')['alt'] if brand_element and brand_element.find('img') else None

                rating_element = item_cell.find('a', class_='item-rating')
                if rating_element:
                    rating = float(rating_element.find('i')['aria-label'].split(' ')[1])
                    rating_count = int(
                        rating_element.find('span').text.replace('(', '').replace(')', '').replace(',', ''))
                else:
                    [rating, rating_count] = self.get_rating_second_structure(soup)

                products_data.append({
                    "title": product_title,
                    "final_price": final_price,
                    "rating": rating,
                    "rating_count": rating_count,
                    "seller": seller
                })

            except Exception as e:
                print(f"Failed to parse product: {e}")
                if product_title:
                    print(f"For Product title: {product_title}")
                continue

        return products_data

    def scrape_paginated(self, db_handler, url):
        soup = url_to_soup.get_soup_from_url(url)
        try:
            pagination_text = soup.find('span', class_='list-tool-pagination-text')
            if pagination_text and '/' in pagination_text.text:
                last_page = int(pagination_text.text.split('/')[1])
            else:
                last_page = 1
        except AttributeError:
            last_page = 1

        base_url = url.split('&')[0]

        for page in range(1, last_page + 1):

            page_url = f"{base_url}&page={page}"
            print(f"Thread {threading.current_thread().name} - Scraping: {page_url}")
            products = self.scrape_page(page_url)
            if products:
                db_handler.insert_products(products)
                with self.lock:
                    self.product_count = db_handler.get_product_count()
                    print(f"Thread {threading.current_thread().name} - Total products in DB: {self.product_count}")
                    if self.product_count >= self.max_products:
                        print(f"Thread {threading.current_thread().name} - Reached product limit. Stopping thread.")
                        return

            time.sleep(0.5)
