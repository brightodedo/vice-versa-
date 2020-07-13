import os, requests
from extras import *

from flask import Flask, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/landing", methods=["POST"])
def landing():
    # collect details from Login Page or Sign up
    error = "*Incorrect Username & Password"
    email = request.form.get("email")
    global username
    username = request.form.get("username")
    #session["username"] = username
    username = username.strip(" ")
    password = request.form.get("password")
    
    return access(error, email, username, password)
    
@app.route("/result", methods=["POST"])
def result():
    items = search(request.form.get("insert"))
    empty = 'Did not find result in search'
    if items == []:
        return render_template("landing.html", empty= empty)
    else:
        return render_template("landing.html", items = items)

@app.route("/result/<string:book_isbn>")
def review(book_isbn):
    goodreads = good_reads_data(book_isbn)
    book_details = db.execute("SELECT * FROM books WHERE isbn=:book_isbn",{"book_isbn":book_isbn}).fetchall()
    reviews = db.execute("SELECT rev_id,isbn,stars,text,username FROM review,users WHERE isbn=:book_isbn AND review.user_id=users.user_id",{"book_isbn":book_isbn}).fetchall()
    #if reviews is empty
    if reviews == None:
        return render_template("review.html", book_details=book_details, goodreads = goodreads)
    #if reviews isn't empty
    else:
        return render_template("review.html", book_details=book_details, goodreads=goodreads,   reviews=reviews)

@app.route("/result/<string:book_isbn>/Reviewed", methods=["POST"])
def reviewed(book_isbn):
    global username 
    goodreads = good_reads_data(book_isbn)
    text = request.form.get("review")
    stars = request.form.get("rats")
    #username = session.get("username")
    user_id = db.execute("SELECT user_id FROM users WHERE username=:username",{"username":username}).fetchone().user_id
    valid = db.execute("SELECT user_id FROM review WHERE user_id=:user_id AND isbn=:book_isbn",{"book_isbn":book_isbn, "user_id":user_id}).fetchone()
    if valid != None:
        #Deny user
        denied = 'You have reviewed this book'
        book_details = db.execute("SELECT * FROM books WHERE isbn=:book_isbn",{"book_isbn":book_isbn}).fetchall()
        reviews = db.execute("SELECT rev_id,isbn,stars,text,username FROM review,users WHERE isbn=:book_isbn AND review.user_id=users.user_id",{"book_isbn":book_isbn}).fetchall()
        return render_template("review.html", book_details=book_details, reviews=reviews, goodreads=goodreads, denied=denied)
    else:
        denied = 'You have reviewed this book'
        db.execute("INSERT INTO review (user_id,isbn,stars,text) VALUES(:user_id,:book_isbn,:stars,:text)",{"user_id":user_id,"book_isbn":book_isbn,"stars":stars,"text":text})
        book_details = db.execute("SELECT * FROM books WHERE isbn=:book_isbn",{"book_isbn":book_isbn}).fetchall()
        reviews = db.execute("SELECT rev_id,isbn,stars,text,username FROM review,users WHERE isbn=:book_isbn AND review.user_id=users.user_id",{"book_isbn":book_isbn}).fetchall()
        db.commit()
        return render_template("review.html", book_details=book_details, goodreads=goodreads, reviews=reviews, denied=denied)

@app.route("/api/<string:book_isbn>")
def book_api(book_isbn):
    #check if book exists
    book = db.execute("SELECT * FROM books WHERE isbn=:book_isbn",{"book_isbn":book_isbn}).fetchone()
    goodreads = good_reads_data(book_isbn)
    if book == None:
        return jsonify({"error": "Invalid book isbn"}), 404
    else:
        return jsonify(
            {"title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": goodreads[1],
            "average_score": goodreads[0]
            }
        )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")