from actions_db import *
from flask import Flask, render_template, request, flash, redirect, url_for
from models import *

app = Flask(__name__)
app.secret_key = 'password'
init_db()

@app.route('/', methods=['GET', "POST"])
@app.route('/products', methods=["GET","POST"])
def products():
    if request.method == "POST":
        name_product = request.form.get('name_product')
        price_product = request.form.get('price_product')
        category_product = request.form.get('category_product')
        company_id = request.form.get('company_id')

        if not product_exists(name_product):
            add_product(name_product, price_product, category_product, company_id)
        else:
            flash(f'product {name_product} is exists')

        return redirect(url_for('products'))
    all_categories = get_all_categories()
    all_companies = get_all_companies()

    choose_category = request.args.get('category', 'All')
    choosed_sort_method = request.args.get('sorted', 'name_asc')
    search = request.args.get('search_by_name', '').strip()
    
    filtered_products = get_specific_products(choosed_sort_method, choose_category, search)

    return render_template('products.html',
                           all_products= filtered_products,
                           all_categories= all_categories,
                           choose_category= choose_category,
                           choosed_sort_method= choosed_sort_method,
                           all_companies = all_companies)

@app.route('/companies', methods= ["GET", "POST"])
def company():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        company_password = request.form.get('password_hash')
        print(company_password, company_name)

        if not company_exists(company_name):
            add_company(company_name, company_password)
        else:
            flash('this company exists')
        return redirect(url_for('products'))

    return render_template('company.html')

@app.route('/delete_product/<name_product>', methods= ["GET", "POST"])
def delete_product(name_product):
    if product_exists(name_product):
        flash(f'product {name_product} deleted')
        delete_product_db(name_product)
    return redirect(url_for('products'))

@app.route('/edit/<name_product>', methods= ["GET", "POST"])
def edit_product(name_product):
    if product_exists(name_product):
        old_category = get_product(name_product).category
        old_price = get_product(name_product).price

    else:
        flash('error in edit')
        return redirect(url_for('products'))

    if request.method == "POST":
        if product_exists(name_product):
            new_category = request.form.get('new_category')
            new_price = request.form.get('new_price')
            edit_product_db(name_product, new_category, new_price)
            flash('product was edited')
            return redirect(url_for('products'))
        else:
            flash('product was not finded')
    return render_template('edit.html', old_product_info= [old_category, old_price])
app.run(debug=True)
