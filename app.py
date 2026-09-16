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

@app.route('/delete/<int: key_product>')
def delete(key_product):
    all_products.pop(key_product)
app.run(debug=True)