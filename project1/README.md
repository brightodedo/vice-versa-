# Project 1

Web Programming with Python and JavaScript

My database URL = postgres://zblaignoegzbgv:b2f7448b899aeee4fcd06c6a165b0237810d0003842f06dd705bc04914db3907@ec2-34-193-117-204.compute-1.amazonaws.com:5432/d6dqc3gep0utvp

Books.csv - comma separated file of various books according to isbn,title,author,year

Python files in this Program{
    1.) application.py - The main application
    2.) import.py - Used to import the books from books.csv into the database(Should be run before application.py)
    3.) extras.py - Contains functions used in application.py
}

Html,css files contained in templates folder{
    1.) layout.html - Contains the basic outline of the website
    2.) index.html - This is the first page to run, also the signup page
    3.) login.html - Already registered users can login using this page
    4.) landing.html - Landing Page after signing up or logging in, when user searches, a table of search results is returned.
    5.) review.html - Reveals a books data and allows the User to add reviews only once.
    6.) about.html - Details about the website
    7.) contact.html - Contains website contact information
    8.) style.css - Contains the styles used in this website
}

"@app.routes" in application.py{
    1.) app.route("/") - corresponds with index.html
    2.) @app.route("/login") - corresponds with login.html
    3.) @app.route("/landing") - corresponds with landing.html
    4.) @app.route("/result") - corresponds with landing.html
    5.) @app.route("/result/<string:book_isbn>") - corresponds with review.html
    6.) @app.route("/result/<string:book_isbn>/Reviewed") - corresponds with review.html
    7.) @app.route("/api/<string:book_isbn>") - Returns json objects or error message
    8.) @app.route("/about") - corresponds with about.hml
    9.) app.route("/contact") - corresponds with contact.hml
}