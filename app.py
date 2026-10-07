from actions_db import *
from flask import Flask, render_template, request, flash, redirect, url_for, session
from models import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'password'
init_db()


def get_current_company():
    return session['current_company']


def is_logged():
    return 'current_company' in session


def is_valid_account(name, password):
    return len(password) >= 6 or not company_exists(name) or name


@app.route('/', methods=['GET', "POST"])
@app.route('/products', methods=["GET","POST"])
def products():
    if not is_logged():
        return redirect(url_for('login'))

    current_company = get_company(get_current_company())
    if not current_company:
        session.pop('current_company', None)
        return redirect(url_for('login'))

    if request.method == "POST":
        name_product = request.form.get('name_product')
        price_product = request.form.get('price_product')
        category_product = request.form.get('category_product')

        if not product_exists(name_product, current_company.id):
            add_product(name_product, price_product, category_product, current_company.id)
        else:
            flash(f'product {name_product} is exists')

        return redirect(url_for('products'))

    all_categories = get_all_categories(current_company.id)
    all_companies = get_all_companies()

    choose_category = request.args.get('category', 'All')
    choosed_sort_method = request.args.get('sorted', 'name_asc')
    search = request.args.get('search_by_name', '').strip()

    filtered_products = get_specific_products(current_company.id, choosed_sort_method, choose_category, search)

    return render_template('products.html',
                           all_products= filtered_products,
                           all_categories= all_categories,
                           choose_category= choose_category,
                           choosed_sort_method= choosed_sort_method,
                           all_companies = all_companies,
                           current_company= get_current_company())


@app.route('/register', methods= ["GET", "POST"])
def register_company():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        company_password = request.form.get('password')

        if is_valid_account(company_name, company_password):
            password_hash = generate_password_hash(company_password)
            add_company(company_name, password_hash)

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

        session['current_company'] = company_name
        flash(f'welcome {company_name}')
        return redirect(url_for('products'))


    return render_template('login.html')


@app.route('/LogOut')
def logout():
    if not is_logged():
        return redirect(url_for('login'))

    session.pop('current_company')
    flash('you LogOut')

    return redirect(url_for('products'))


@app.route('/delete_product/<name_product>', methods= ["GET", "POST"])
def delete_product(name_product):
    if not is_logged():
        return redirect(url_for('login'))

    current_company = get_company(get_current_company())

    if product_exists(name_product, current_company.id):
        flash(f'product {name_product} deleted')
        delete_product_db(name_product, current_company.id)

    return redirect(url_for('products'))


@app.route('/edit/<name_product>', methods= ["GET", "POST"])
def edit_product(name_product):
    if not is_logged():
        return redirect(url_for('login'))

    current_company = get_company(get_current_company())

    if product_exists(name_product, current_company.id):
        old_category = get_product(name_product, current_company.id).category
        old_price = get_product(name_product, current_company.id).price
    else:
        flash('error in edit')
        return redirect(url_for('products'))

    if request.method == "POST":
        if product_exists(name_product, current_company.id):
            new_category = request.form.get('new_category')
            new_price = request.form.get('new_price')
            edit_product_db(name_product, new_category, new_price, current_company.id)
            flash('product was edited')
            return redirect(url_for('products'))
        else:
            flash('product was not finded')
    return render_template('edit.html', old_product_info= [old_category, old_price])

@app.route('/profile', methods= ["GET", "POST"])
def profile():
    company = get_company(get_current_company())
    products_company = get_company_products(company.id)
    return render_template('profile.html', current_company=company, products_company= products_company)

@app.route('/new_name', methods= ["GET", "POST"])
def new_name():
    company = get_company(get_current_company())
    if not company:
        session.pop('current_company')
        return redirect(url_for('login'))

    if request.method == "POST":
        new_name_company = request.form.get('new_name')
        if new_name_company and new_name_company not in get_all_company_names():
            update_company_name(company.name, new_name_company)
            session['current_company'] = new_name_company
            flash('name was updated')
            return redirect(url_for('profile'))
    return render_template('new_name.html')

@app.route('/new_password', methods= ["GET", "POST"])
def new_password():
    company = get_company(get_current_company())
    if request.method == "POST":
        old_password = request.form.get('old_password')
        if not check_password_hash(company.password, old_password):
            flash('uncorrect old password')
            return redirect(url_for('new_password'))
        new_password = request.form.get('new_password')
        again_new_password = request.form.get('again_new_password')
        if new_password != again_new_password:
            flash('The new password does not match the repeated password')
            return redirect(url_for('new_password'))
        update_company_password(company.name, new_password)
    return render_template('new_password.html')

app.run(debug=True)
