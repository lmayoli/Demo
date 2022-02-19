from datetime import timedelta
from flask import Flask, redirect, render_template, url_for, request, session, flash
from flask_sqlalchemy  import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.secret_key = "KFC"
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    number = db.Column("number", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    def __init__(self,name,email, number):
        self.name = name 
        self.email = email
        self.number = number
        

@app.route("/")
def home():
   
    return render_template("index.html")

@app.route("/login", methods= ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        
        return redirect(url_for("user"))
    else:
        return render_template("login.html")

@app.route("/user", methods= ["POST","GET"])
def user():

 number=None
 if "user" in session:
        user = session["user"]
        if request.method == "POST":
            number = request.form["number"]
            session["number"] = number
            flash("number entered")
        else:
            if "number" in session:
                number = session["number"]
        return render_template("user.html", number=number)
 else:
    flash("you are not logged in ")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("logout successful", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)