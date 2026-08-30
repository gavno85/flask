from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

current_hour = datetime.now().hour
if 11 < current_hour < 22:
    work_status = "working"

else:
    work_status = "closed"

@app.route('/')
def homepage_func():
    return render_template("homepage.html", work_status= work_status)

menu = {
	"Капучино": 80,
	"Лате": 85,
	"Еспресо": 60,
	"Чізкейк": 120,
	"Панкейки": 95
}
current_day = datetime.now().weekday()

@app.route('/menu')
def menu_func():
    return render_template("menu.html", menu= menu, current_day= current_day)













app.run(debug=True)