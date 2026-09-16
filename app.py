from os import name

from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'password'
all_products = {}

@app.route('/delete/<name_product>')
def delete():
    pass

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

    return render_template('products.html', all_products=all_products)

@app.route('/delete_product/<key_product>')
def delete_product(key_product):
    if key_product in all_products.keys():
        deleted_product = all_products.pop(key_product)
        flash(f'product {deleted_product} deleted')
    return redirect(url_for('products'))

@app.route('/edit/<name_product>', methods= ["GET", "POST"])
def edit_product(name_product):
    product = all_products[name_product]
    if product:
        old_category = all_products.get(name_product)['category']
        old_price = all_products.get(name_product)['price']
    else:
        old_category = 'not finded'
        old_price = 'not finded'

    if request.method == "POST":
        if name_product in all_products.keys():
            new_category = request.form.get('new_category')
            new_price = request.form.get('new_price')
            product = {'category': new_category, 'price': new_price}
            flash('product was edited')
            return redirect(url_for('products'))
        else:
            flash('product was not finded')
    return render_template('edit.html', old_category= old_category, old_price= old_price)
app.run(debug=True)