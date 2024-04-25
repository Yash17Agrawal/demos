import json

class Storage:
    def __init__(self):
        # Initialize the sdk with creds
        pass

    def _save_in_db(self, items: list):
        pass
    
    def _save_in_blob_storage(self, items:list):
        pass

    def _save_in_file(self, items: list):
        # Save scraped data to a JSON file
        with open('catalogue_data.json', 'w') as json_file:
            products_dict = [product.to_dict()
                             for product in items]
            json.dump(products_dict, json_file, indent=4)

    def save(self, items:list):
        self._save_in_file(items)
        # uncomment to change the mode of notification
        # self._save_in_db(items)

