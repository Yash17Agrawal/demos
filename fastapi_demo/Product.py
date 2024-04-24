class Product:
    def __init__(self, title: str, price: float, image_url: str):
        if not isinstance(title, str) or not title:
            raise ValueError("Name must be a non-empty string")
        if (not isinstance(price, float) and not isinstance(price, int))or price <= 0:
            raise ValueError("Price must be a positive float")
        if not isinstance(image_url, str) or not image_url.startswith("http"):
            raise ValueError("Image URL must be a valid HTTP URL")
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