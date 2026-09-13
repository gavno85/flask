from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "asdad"

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        user_phone = request.form.get('phone')
        if len(user_phone) != 12 or user_phone[:4] != "+380":
            flash("input incorrect number")
        else:
            flash('you registered')
            return redirect(url_for('register'))
        
    return render_template('register.html')

app.run(debug=True)
