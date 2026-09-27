from models import Product, Company
# create
def add_product(name, price, category, company_id):
    Product.create(name= name, price= price, category= category, company_id= company_id)

def add_company(company_name, password_hash):
    Company.create(company= company_name, password_hash= password_hash)
# read
def product_exists(name: str) -> bool:
    return Product.select(Product.name).where(Product.name == name).exists()

def company_exists(name: str) -> bool:
    return Company.select(Company.company).where(Company.company == name).exists()

def get_all_companies():
    return list(Company.select())

def get_all_categories() -> list:
    return list(Product.select(Product.category).distinct())

def get_products_by_categories(category: str) -> list:
    return list(Product.select().where(Product.category == category))

def get_specific_products(type_sort= 'name_asc', category= 'All', search = ''):
    product = Product.select()
    if category != "All":
        product = product.where(Product.category == category)

    if search:
        product = product.where(Product.name.contains(search))

    if type_sort == 'name_asc':
        sorted_product_list = product.order_by(Product.name.asc())
    elif type_sort == 'name_desc':
        sorted_product_list = product.order_by(Product.name.desc())

    elif type_sort == 'price_asc':
        sorted_product_list = product.order_by(Product.price.asc())
    else:
        sorted_product_list = product.order_by(Product.price.desc())

    return sorted_product_list

def get_all_products() -> list:
    return list(Product.select())

def get_product(name):
    return Product.get(Product.name == name)

# delete
def delete_product_db(name):
    Product.delete().where(Product.name == name).execute()

# update
def edit_product_db(name, category, price):
    if product_exists(name):
        Product.update(category=category, price=price).where(Product.name == name).execute()
