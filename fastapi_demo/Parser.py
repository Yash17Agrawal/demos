from Product import Product

import json

class Parser:
    """A simple parser class"""
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

    def scrape(self) -> list[Product]:
        catalogue_data = [{"name": "John", "age": 30, "img_url": "https://1.com/shop/"},
                      {"name": "Alice", "age": 25, "img_url": "https://2.com/shop/"}]
        if catalogue_data:
            self.store_data(catalogue_data)
        return 'hello world'

    def _validate(self, Product) -> bool:
        return True

    def store_data(self, data: list) -> None:
        valid_scrapped_products = []
        invalid_scrapped_products = []
        for product_items in data:
            product =Product(product_items['name'], product_items['age'], product_items['img_url'])
            is_valid = self._validate(product)
            if is_valid:
                valid_scrapped_products.append(product)
            else:
                invalid_scrapped_products.append(product)

        # Save scraped data to a JSON file
        with open('catalogue_data.json', 'w') as json_file:
            products_dict = [product.to_dict() for product in valid_scrapped_products]
            json.dump(products_dict, json_file, indent=4)
        print("Catalogue data saved to catalogue_data.json")
        print("{} products scrapped".format(len(valid_scrapped_products)))
        self._notify(1,1)
        return 'hello world'

    def _notify(self, success_count, failed_count) -> None:
        return 'hello world'
