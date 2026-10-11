from models import Product, Company
#product
def add_product(name, price, category, company_id):
    Product.create(name= name, price= price, category= category, company= company_id)
def get_all_products(company_id) -> list:
    return list(Product.select().where(Product.company == company_id))

def get_product(name, company_id):
    return Product.get_or_none((Product.name == name) & (Product.company == company_id))

def product_exists(name: str, company_id) -> bool:
    return Product.select(Product.name).where((Product.name == name) & (Product.company == company_id)).exists()

def get_specific_products(company_id, type_sort= 'name_asc', category= 'All', search = ''):
    product = Product.select().where(Product.company == company_id)
    if category != "All":
        product = product.where(Product.category == category)

    if search:
        product = product.where(Product.name.contains(search))

    if type_sort == 'name_asc':
        product = product.order_by(Product.name.asc())
    elif type_sort == 'name_desc':
        product = product.order_by(Product.name.desc())

    elif type_sort == 'price_asc':
        product = product.order_by(Product.price.asc())

    else:
        product = product.order_by(Product.price.desc())

    return product

def get_products_by_categories(category, company_id):
    return list(Product.select().where((Product.category == category) & (Product.company == company_id)))

def delete_product_db(name, company_id):
    Product.delete().where((Product.name == name) & (Product.company == company_id)).execute()

def delete_product_by_company(company_id):
    Product.delete().where(Product.company == company_id).execute()

def edit_product_db(name, category, price, company_id):
    if product_exists(name, company_id):
        (Product.update(category=category, price=price)
         .where((Product.name == name) & (Product.company == company_id)).execute())

def get_all_categories(company_id) -> list:
    return list(Product.select(Product.category).where(Product.company == company_id).distinct())

#company
def add_company(company_name, password_hash):
    Company.create(name= company_name, password= password_hash)

def company_exists(name: str) -> bool:
    return Company.select(Company.name).where(Company.name == name).exists()

def get_company(name):
    return Company.get_or_none(Company.name == name)

def get_company_products(company_id):
    return Product.select().where(Product.company == company_id)

def get_all_companies():
    return list(Company.select())

def get_all_company_names():
    return list(Company.select(Company.name))

def get_company_by_id(company_id):
    return Company.get_or_none(Company.id == company_id)

def delete_company(name):
    Company.delete().where(Company.name == name).execute()

def update_company_name(old_name, new_name):
    Company.update(name= new_name).where(Company.name == old_name).execute()

def update_company_password(company_name, new_password):
    Company.update(password= new_password).where(Company.name == company_name).execute()
