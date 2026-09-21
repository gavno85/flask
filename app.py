from flask import Flask, render_template, request, flash, redirect, url_for
from models import *

app = Flask(__name__)
app.secret_key = 'password'
init_db()
all_products = {}

def sort_products(choosed_sort_method : str, products: dict):
    if choosed_sort_method == 'name_asc':
        sorted_products = dict(sorted(products.items(),
                                      key=lambda product: product[0]))

    elif choosed_sort_method == 'name_desc':
        sorted_products = dict(sorted(products.items(),
                                      key=lambda product: product[0], reverse=True))

    elif choosed_sort_method == 'price_asc':
        sorted_products = dict(sorted(products.items(),
                                      key=lambda product: int(product[1].get('price'))))

    else:
        sorted_products = dict(sorted(products.items(),
                                      key=lambda product: int(product[1].get('price')), reverse=True))
    return sorted_products

def search_by_name(products, name):
    if name and name != 'All':
        searched_products = {
            name_search: product_info for name_search, product_info in products.items()
            if name.lower() in name_search.lower()
        }
    else:
        searched_products = products
    return searched_products

def filter_product(category, products):
    if category == "All":
        filtered_products = products
    else:
        filtered_products = {name:product_info for name, product_info in products.items()
                             if product_info.get('category') == category}
    return filtered_products


@app.route('/', methods=['GET', "POST"])
@app.route('/products', methods=["GET","POST"])
def products():
    if request.method == "POST":
        name_product = request.form.get('name_product')
        price_product = request.form.get('price_product')
        category_product = request.form.get('category_product')

        if name_product not in all_products.keys():
            all_products[name_product] = {'category': category_product, 'price': price_product}
        else:
            flash(f'product {name_product} is exists')

        return redirect(url_for('products'))
    all_categories = [product_info.get('category') for product_info in all_products.values()]

    choose_category = request.args.get('category', 'All')
    filtered_products = filter_product(choose_category, all_products)

    choosed_sort_method = request.args.get('sorted', 'name_asc')
    sorted_products = sort_products(choosed_sort_method, filtered_products)

    search = request.args.get('search_by_name', '').strip()
    searched_products = search_by_name(sorted_products, search)

    return render_template('products.html',
                           all_products= searched_products,
                           all_categories= all_categories,
                           choose_category= choose_category,
                           choosed_sort_method= choosed_sort_method)

@app.route('/delete_product/<name_product>')
def delete_product(name_product):
    if name_product in all_products.keys():
        deleted_product = all_products.pop(name_product)
        flash(f'product {deleted_product} deleted')
    return redirect(url_for('products'))

@app.route('/edit/<name_product>', methods= ["GET", "POST"])
def edit_product(name_product):
    product = all_products.get(name_product)
    if product:
        old_category = all_products.get(name_product)
        old_price = all_products.get(name_product)
        if old_category is not None:
            old_category = old_category['category']
        if old_price is not None:
            old_price = old_price['price']
    else:
        flash('error in edit')
        return redirect(url_for('products'))

    if request.method == "POST":
        if name_product in all_products.keys():
            new_category = request.form.get('new_category')
            new_price = request.form.get('new_price')
            all_products[name_product] = {'category': new_category, 'price': new_price}
            flash('product was edited')
            return redirect(url_for('products'))
        else:
            flash('product was not finded')
    return render_template('edit.html', old_category= old_category, old_price= old_price)
app.run(debug=True)