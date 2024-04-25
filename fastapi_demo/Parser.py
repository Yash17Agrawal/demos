from typing import List

from bs4 import BeautifulSoup
import requests
from Product import Product

import json

class Parser:
    """
        Parser class to scrape the remote
        remote_url: str: URL to scrape
        number_of_pages: int: Number of pages to scrape
        retry_count: int: Number of retries to make
    """
    remote_url = "https://dentalstall.com/shop/"
    number_of_pages = 5
    retry_count = 5

    def __init__(self, url=None, number_of_pages=None, retry_count=None) -> None:
        if url:
            self.remote_url = url
        if number_of_pages:
            self.number_of_pages = number_of_pages
        if retry_count:
            self.retry_count = retry_count

    def scrape(self) -> List[Product]:
        """
            Scrape the remote URL and stores the data in catalogue_data.json
        """
        # catalogue_data = [{"name": "John", "price": 30, "img_url": "https://1.com/shop/"},
        #                   {"name": "Alice", "price": 25, "img_url": "https://2.com/shop/"},
        #                   {"name": "Alice", "price": 0, "img_url": "https://2.com/shop/"}]
        
        response = requests.get(self.remote_url)
        if response.status_code == 200:
        # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract product information
            products = []

            # Find all product elements on the page
            product_cards = soup.find_all('div', class_='product-inner')

            for card in product_cards[:1]:
                thumbnail = card.find('img', class_='attachment-woocommerce_thumbnail')["data-lazy-src"]
                # Extract product name
                title = card.find('h2', class_='woo-loop-product__title').find('a').text.strip()
                # Extract product price
                price = card.find('ins').find('span').find("bdi").text.strip()

                # Remove the currency symbol (₹) and any non-numeric characters
                numeric_value = ''.join(filter(str.isdigit, price))

                # Convert the numeric value to an integer
                price = int(numeric_value)


                # Append product information to the list
                products.append({'name': title, 'price': price, 'image_url': thumbnail})

            print(products)
        else:
            # Print an error message if the request was unsuccessful
            print(f"Failed to retrieve data from {self.remote_url}. Status code: {response.status_code}")
        if products:
            self.store_data(products)

    def store_data(self, data: List[dict]) -> None:
        valid_scrapped_products: List[Product] = []
        invalid_scrapped_products: List[dict] = []
        for product_items in data:
            try:
                product = Product(
                    product_items['name'], product_items['price'], product_items['image_url'])
                valid_scrapped_products.append(product)
            except Exception as e:
                print(e)
                invalid_scrapped_products.append(product_items)

        # Save scraped data to a JSON file
        with open('catalogue_data.json', 'w') as json_file:
            products_dict = [product.to_dict()
                             for product in valid_scrapped_products]
            json.dump(products_dict, json_file, indent=4)
        self._notify(len(valid_scrapped_products),
                     len(invalid_scrapped_products))

    def _notify(self, success_count, failed_count) -> None:
        print("Catalogue data saved to catalogue_data.json")
        print("{} products scrapped successfully and {} failed".format(
            success_count, failed_count))
