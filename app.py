from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template("welcome.html", name = "Artur")


app.run(debug=True)
