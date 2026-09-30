from actions_db import *
from flask import Flask, render_template, request, flash, redirect, url_for
from models import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'password'
init_db()
current_company = None

@app.route('/', methods=['GET', "POST"])
@app.route('/products', methods=["GET","POST"])
def products():
    if request.method == "POST":
        name_product = request.form.get('name_product')
        price_product = request.form.get('price_product')
        category_product = request.form.get('category_product')
        company_product = get_company(current_company)

        if not product_exists(name_product):
            add_product(name_product, price_product, category_product, company_product)
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
                           all_companies = all_companies,
                           current_company= current_company)

@app.route('/register', methods= ["GET", "POST"])
def register_company():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        company_password = request.form.get('password')

        if is_valid_account(company_name, company_password):
            password_hash = generate_password_hash(company_password)
            add_company(company_name, password_hash)
            global current_company
            current_company = company_name
        else:
            flash('password shorter than 6, login is not exists or company with this name exists')
        return redirect(url_for('products'))

    return render_template('register.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        company_password = request.form.get('password')
        if not company_exists(company_name):
            flash(f'company {company_name} is not exists')
            return redirect(url_for('register_company'))

        company = get_company(company_name)
        if not check_password_hash(company.password, company_password):
            flash('incorrect password')
            return redirect(url_for('login'))
        else:
            global current_company
            current_company = company_name
            flash(f'welcome {company_name}')
            return redirect(url_for('products'))

    return render_template('login.html')

@app.route('/LogOut')
def logout():
    global current_company
    delete_company(current_company)
    current_company = None
    flash('you LogOut')
    return redirect(url_for('products'))

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

def is_valid_account(name, password):
    return len(password) >= 6 or not company_exists(name) or name
