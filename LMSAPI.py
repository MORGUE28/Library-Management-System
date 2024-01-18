from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
import pandas as pd
import os

# Creating the database engine
engine = create_engine('sqlite:///library.db', echo=True)

# Creating a base class for declarative models
Base = declarative_base()

# Defining the Book model
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    checked_out = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='checked_books')

# Defining the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    checked_books = relationship('Book', back_populates='user')

# Creating the tables in the database
Base.metadata.create_all(engine)

# FastAPI app instance
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Function to load data from CSV or create an empty DataFrame
def load_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

# Function to save data to CSV
def save_csv(data, file_path):
    data.to_csv(file_path, index=False)

# Function to add a new book to the library
def add_book(db: Session, title: str, author: str):
    new_book = Book(title=title, author=author)
    db.add(new_book)
    db.commit()
    save_csv(pd.read_sql_table('books', engine), 'library.csv')

# Function to delete a book from the library
def delete_book(db: Session, book_id: int):
    book = db.query(Book).get(book_id)
    if book:
        db.delete(book)
        db.commit()
        save_csv(pd.read_sql_table('books', engine), 'library.csv')
    else:
        raise HTTPException(status_code=404, detail="Book not found")

# Function to edit the details of an existing book
def edit_book(db: Session, book_id: int, title: str = None, author: str = None):
    book = db.query(Book).get(book_id)
    if book:
        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        db.commit()
        save_csv(pd.read_sql_table('books', engine), 'library.csv')
    else:
        raise HTTPException(status_code=404, detail="Book not found")

# Function to check out a book for a particular user
def check_out_book(db: Session, book_id: int, user_id: int):
    book = db.query(Book).get(book_id)
    user = db.query(User).get(user_id)
    if book and user:
        book.checked_out = user.id
        db.commit()
        save_csv(pd.read_sql_table('books', engine), 'library.csv')
    else:
        raise HTTPException(status_code=404, detail="Book or User not found")

# Function to get all users who have checked out any book
def get_checked_out_users(db: Session):
    checked_out_users = db.query(User).join(Book).filter(Book.checked_out.isnot(None)).distinct().all()
    return checked_out_users

def add_user(db: Session, name: str):
    new_user = User(name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  
    return {"message": "User added successfully","user_id": new_user.id}

# Function to get borrowed books by a specific user
def get_borrowed_books_by_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    if user:
        borrowed_books = user.checked_books
        return [{"id": book.id, "title": book.title, "author": book.author} for book in borrowed_books]
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Function to get all books available in the library
def get_all_books(db: Session):
    all_books = db.query(Book).all()
    return [{"id": book.id, "title": book.title, "author": book.author} for book in all_books]

# FastAPI endpoints
@app.post("/books/")
def create_book(title: str, author: str, db: Session = Depends(get_db)):
    add_book(db, title, author)
    return {"message": "Book added successfully"}

@app.post("/users/")
def create_user(name: str, db: Session = Depends(get_db)):
    return add_user(db, name)

@app.delete("/books/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db)):
    delete_book(db, book_id)
    return {"message": "Book deleted successfully"}

@app.put("/books/{book_id}")
def modify_book(book_id: int, title: str, author: str, db: Session = Depends(get_db)):
    edit_book(db, book_id, title, author)
    return {"message": "Book edited successfully"}

@app.get("/books/")
def view_all_books(db: Session = Depends(get_db)):
    all_books = get_all_books(db)
    return {"all_books": all_books}

@app.post("/books/{book_id}/checkout/{user_id}")
def checkout_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    check_out_book(db, book_id, user_id)
    return {"message": "Book checked out successfully"}

@app.get("/checked-out-users/")
def get_checked_out_users_endpoint(db: Session = Depends(get_db)):
    checked_out_users = get_checked_out_users(db)
    return {"checked_out_users": [{"id": user.id, "name": user.name} for user in checked_out_users]}

# FastAPI endpoint to get borrowed books by a specific user
@app.get("/users/{user_id}/borrowed-books/")
def get_borrowed_books(user_id: int, db: Session = Depends(get_db)):
    borrowed_books = get_borrowed_books_by_user(db, user_id)
    return {"borrowed_books": borrowed_books}