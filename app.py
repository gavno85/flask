from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "asdad"
all_register= []

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        user_phone = request.form.get('phone')
        if len(user_phone) != 13 or user_phone[:4] != "+380":
            flash("input incorrect number")
        else:
            all_register.append({'username': username, 'user_phone': user_phone})
            flash('you registered')
            return redirect(url_for('main'))
        
    return render_template('register.html')


@app.route('/admin')
def admin():
    return render_template('admin.html', all_register= all_register)

@app.route('/delete/<int:index_wish>')
def delete(index_wish):
    all_register.pop(index_wish)
    return redirect(url_for('admin'))
app.run(debug=True)
