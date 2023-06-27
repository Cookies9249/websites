# pip3 install Flask Flask-SQLAlchemy

from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.app_context().push()

class Todo(db.Model):
    # name = db.Column(datatype)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    todo_list = db.session.query(Todo).filter(Todo.user_id == user_id)

    if todo_list:
        return render_template("index.html", todo_list=todo_list)
    else:
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    # user = Users(id=2, username="1", password="2")
    # db.session.add(user)

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("login.html", error="Enter Username")
        if not request.form.get("password"):
            return render_template("login.html", error="Enter Password")

        user_info = db.session.query(Users).filter(Users.username == request.form.get("username")).first()

        if not user_info:
            return render_template("login.html", error="Invalid Username")
        if not user_info.password == request.form.get("password"):
            return render_template("login.html", error="Invalid Password")

        if user_info.password == request.form.get("password"): print(f'Login success {user_info.id}')
        session["user_id"] = user_info.id

        db.session.commit()
        return redirect("/")

    return render_template("login.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        title = request.form.get("title")
        user_id = session["user_id"]
        new_todo = Todo(title=title, user_id=user_id, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    return redirect("/")

@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
@login_required
def update(todo_id):
    if request.method == "POST":
        todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
        todo.complete = not todo.complete
        db.session.commit()
    return redirect("/")

@app.route("/delete/<int:todo_id>", methods=["GET", "POST"])
@login_required
def delete(todo_id):
    if request.method == "POST":
        todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")