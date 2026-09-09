from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "1234"
all_wishes = []

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        added_wish = request.form.get('wish')
        if added_wish:
            added_wish = added_wish.lower()

            if added_wish not in all_wishes:
                all_wishes.append(added_wish)
                flash('wish added!')
            else:
                flash('wish already exists')
        else:
            flash('wish must be')
        return redirect(url_for("main"))

    exists_wish = request.args.get('find')
    if exists_wish:
        if exists_wish in all_wishes:
            flash('this wish is in list')
        else:
            flash('this wish is not in list')

    return render_template('main.html', all_wishes= all_wishes)

app.run(debug=True)