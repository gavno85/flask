from flask import Flask

app = Flask(__name__)

@app.route('/delete/<int:index_wish>')
def delete(index_wish):
    flash(f'wish {all_wishes[index_wish]} deleted')
    all_wishes.pop(index_wish)
    return redirect(url_for('main'))

app.run(debug=True)