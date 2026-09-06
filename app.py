from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def temperature():
    temperature_f = None
    temperature_c = request.args.get('temperature')
    if temperature_c:
        temperature_f = float(temperature_c) * 1.8 + 32
    return render_template("temperature.html", temperature_f= temperature_f, temperature_c = temperature_c)

app.run(debug=True)