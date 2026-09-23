from app import all_products
from models import Product
# create
def add_product(name, price, category):
    Product.create(name= name, price= price, category= category)
# read
def get_product(name: str):
    return {product for product in all_products if name == product.name}

def product_exists(name: str) -> bool:
    return Product.select(Product.name).where(Product.name == name).exists()

def get_all_categories():
    return list(Product.select(Product.category))

def get_products_by_categories(category: str):
    return list(Product.select(Product.name).where(Product.category == category))

# def sorted_products(products: dict):

def get_product_by_name(name):
    return Product.select(Product.name).where(Product.name == name).scalar()

def get_products():
    return list(Product.select(Product.name))

# delete
def delete_product(name):
    Product.delete(Product.name)

# update
def edit_product(name, category, price):
    if product_exists(name):
        all_products[name] = {'category': category, 'price': price}
