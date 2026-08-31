from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def homepage_func():
    return render_template("homepage.html", current_hour= datetime.now().hour)

menu = {
	"Капучино": 80,
	"Лате": 85,
	"Еспресо": 60,
	"Чізкейк": 120,
	"Панкейки": 95
}

@app.route('/menu')
def menu_func():
    return render_template("menu.html", menu= menu, current_day= datetime.now().weekday())

app.run(debug=True)