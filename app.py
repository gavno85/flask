from flask import Flask, render_template
from book_list import books

app = Flask(__name__)

@app.route("/")
def book():
    return render_template("books.html", book_list= books)

app.run(debug=True)