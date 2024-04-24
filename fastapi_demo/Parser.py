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

    def scrape(self) -> list[Product]:
        """
            Scrape the remote URL and stores the data in catalogue_data.json
        """
        catalogue_data = [{"name": "John", "price": 30, "img_url": "https://1.com/shop/"},
                          {"name": "Alice", "price": 25, "img_url": "https://2.com/shop/"},
                          {"name": "Alice", "price": 0, "img_url": "https://2.com/shop/"}]
        if catalogue_data:
            self.store_data(catalogue_data)
        return 'hello world'

    def store_data(self, data: list) -> None:
        valid_scrapped_products: list[Product] = []
        invalid_scrapped_products: list[dict] = []
        for product_items in data:
            try:
                product = Product(
                    product_items['name'], product_items['price'], product_items['img_url'])
                valid_scrapped_products.append(product)
            except Exception as e:
                invalid_scrapped_products.append(product_items)

        # Save scraped data to a JSON file
        with open('catalogue_data.json', 'w') as json_file:
            products_dict = [product.to_dict()
                             for product in valid_scrapped_products]
            json.dump(products_dict, json_file, indent=4)
        print("Catalogue data saved to catalogue_data.json")
        self._notify(len(valid_scrapped_products),
                     len(invalid_scrapped_products))

    def _notify(self, success_count, failed_count) -> None:
        print("{} products scrapped successfully and {} failed".format(
            success_count, failed_count))
