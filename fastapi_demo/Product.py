class Product:
    def __init__(self, title: str, price: float, image_url: str):
        self.title = title
        self.price = price
        self.image_url = image_url

    def __repr__(self):
        return f"Product(title={self.title}, price={self.price}, image_url={self.image_url})"

    def to_dict(self):
        return {
            'product_title': self.title,
            'product_price': self.price,
            'path_to_image': self.image_url
        }