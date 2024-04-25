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
    number_of_pages = 2
    retry_count = 5
    caching = {}

    def __init__(self, url=None, number_of_pages=None, retry_count=None) -> None:
        if url:
            self.remote_url = url
        if number_of_pages:
            self.number_of_pages = number_of_pages
        if retry_count:
            self.retry_count = retry_count
    
    def _scrape(self, url, products, attempt=1) -> List[Product]:
        print("Parsing {}, attempt: {}".format(url, attempt))
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all product elements on the page
                product_cards = soup.find_all('div', class_='product-inner')
                
                for card in product_cards:
                    thumbnail = card.find('img', class_='attachment-woocommerce_thumbnail')["data-lazy-src"]
                    # Extract product name
                    title = card.find('h2', class_='woo-loop-product__title').find('a').text.strip()
                    # Extract product price
                    price = card.find('ins')
                    if price:
                        price = price.find('span').find("bdi").text.strip()
                    else:
                        price = card.find('span', class_='woocommerce-Price-amount').find('bdi').text.strip()
                    # Remove the currency symbol (₹) and any non-numeric characters
                    numeric_value = ''.join(filter(str.isdigit, price))

                    # Convert the numeric value to an integer
                    price = int(numeric_value)


                    # Append product information to the list
                    products.append({'name': title, 'price': price, 'image_url': thumbnail})
                if products:
                    self.store_data(products)
                # Find the link to the next page
                pagination = soup.find("nav", class_="woocommerce-pagination").find("ul").find_all("li")
                for line in pagination:
                    current_page = line.find('span', class_='current')
                    if current_page:
                        current_page = int(current_page.text.strip())
                        if current_page < self.number_of_pages:
                            # Get the URL of the next page
                            next_page_url = line.find_next_sibling().find("a")['href']
                            # Make an HTTP request to the URL of the next page
                            return self._scrape(next_page_url, products)
                        return
            else:
                raise Exception(f"Failed to retrieve data from {self.remote_url}. Status code: {response.status_code}")
        except Exception as e:
            print(e)
            if attempt < self.retry_count:
                # Retry the request if it fails
                return self._scrape(url, products, attempt + 1)
            else:
                print("Failed to retrieve data from {}. Max retries exceeded.".format(url)) 


    def scrape(self) -> List[Product]:
        products = []
        """
            Scrape the remote URL and stores the data in catalogue_data.json
        """
        # products = [{"name": "John", "price": 30, "image_url": "https://1.com/shop/"},
        #                   {"name": "Alice", "price": 25, "image_url": "https://2.com/shop/"},
        #                   {"name": "Alice", "price": 0, "image_url": "https://2.com/shop/"}]
        self._scrape(self.remote_url, products)
        
    def _get_cache_key(self, product:Product):
        return "{}_{}".format(product.title, product.image_url)

    def store_data(self, data: List[dict]) -> None:
        valid_scrapped_products: List[Product] = []
        invalid_scrapped_products: List[dict] = []
        for product_items in data:
            try:
                product = Product(
                    product_items['name'], product_items['price'], product_items['image_url'])
                if self._get_cache_key(product) in self.caching.keys() and self.caching[self._get_cache_key(product)] == product.price :
                    # Dont want to re-trigger db updated if price is not changed
                    print("skipping update for product: {}".format(product.title))
                    continue
                valid_scrapped_products.append(product)
                self.caching[self._get_cache_key(product)] = product.price
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
