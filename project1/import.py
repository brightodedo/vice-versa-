import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("CREATE TABLE books(ISBN VARCHAR PRIMARY KEY, title VARCHAR, author VARCHAR, year INTEGER)")
    book = open("books.csv", 'r')
    book_item = csv.reader(book)
    next(book_item)
    for isbn, title, author, year in book_item: 
        db.execute("INSERT INTO books(ISBN, title, author, year) VALUES( :isbn, :title, :author, :year)",{"isbn": isbn, "title":title, "author":author, "year": int(year)})
    db.commit()

def users():
    db.execute("CREATE TABLE users(user_id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
    db.commit()

def review():
    db.execute("CREATE TABLE review(rev_id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users ,ISBN VARCHAR REFERENCES books, stars FLOAT NOT NULL, text VARCHAR NOT NULL)")
    db.commit()

if __name__ == "__main__":
    main()
    users()
    review()