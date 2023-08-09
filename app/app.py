from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost/pyscript"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

@app.route("/")
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return render_template("index.html", logged_in=True)
        else:
            return render_template("index.html", logged_in=False)
    else:
        return render_template("index.html", logged_in=False)

if __name__ == "__main__":
    app.run(debug=True)
