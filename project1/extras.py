import os, requests 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, session, render_template, request

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def good_reads_data(book_isbn):
    """ 
    returns book average rating and number of ratings recieved in a tuple from good reads website 
    like ('book average rating', 'number of ratings recieved')
    """
    KEY = 'RmzbF6LAY84EBU0rdRMN3Q'
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": book_isbn})
    goodreads_data=goodreads.json()
    goodreads_data_set = goodreads_data['books'][0]
    return (goodreads_data_set["average_rating"], goodreads_data_set["work_ratings_count"])



def access(error, email, username, password):

    """
    Collects error message, email, username, password inputted and returns the appropriate webpage
    """

    # Checking if from Login page or Sign up page using email variable
    if email is not None:
        # from Sign up page, email isn't set to none type

        #Check if username already exists
        name_pass = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        if name_pass is not None:
            return render_template("index.html", fault="username taken")

        #Add details to database
        else:
            db.execute("INSERT INTO users(username, password) VALUES( :username, :password)", {"username":username, "password":password})
            db.commit()
            return render_template("landing.html")
    else:
        #from login page, email is none.

        #Check if Username exists
        name_pass = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        if name_pass != None:
            if username != name_pass.username:
                return render_template("login.html", error=error)
        else:
            return render_template("login.html", error = error)
        #Check if Password exists
        pass_pass = db.execute("SELECT password FROM users WHERE username=:username", {"username":username}).fetchone()
        if password != pass_pass.password:
            return render_template("login.html", error = error)

        #if both username and password exist
        return render_template("landing.html")


def search(search_word):
    """ 
    Searches for user input in the book database and returns it in a list of tuples containing each book's title, author,
    isbn respectively
    eg [('title1', 'author1', 'isbn1'), ('title2', 'author2','isbn2')]
    """

    search_word = '%' + search_word + '%'
    items = db.execute("SELECT title,author,isbn FROM books WHERE title LIKE :word OR author LIKE :word OR isbn LIKE :word ", {"word":search_word}).fetchall()
    return items