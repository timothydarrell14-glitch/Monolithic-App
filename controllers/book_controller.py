# this is where we will define the logic for handling book-related requests - controller layer
from models.book import Book 
from extensions import db

class BookController: 
    # Define a method to get all books from the database
    @classmethod
    def get_all_books(cls): 
        "SELECT * FROM books"
        return Book.query.all()
    # Define a method that creates a new book in the database
    @classmethod
    def create_book(cls, book_data): 
        "insert into books (title, author) values (:title, :author)"
        new_book = Book(title=book_data["title"], author=book_data["author"])
        db.session.add(new_book)
        db.session.commit()
        return new_book  # return the ORM object; the route decides how to serialize it

    # Define a method that retrieves a book by its ID from the database
    @classmethod
    def get_book_by_id(cls, book_id): 
        "SELECT * FROM books WHERE id = :book_id"
        return Book.query.filter_by(id=book_id).first()
    # Define a method that updates a book's information in the database
    @classmethod
    def update_book(cls, book_id, book_data): 
        book = cls.get_book_by_id(book_id=book_id)
        if book:
            book.title = book_data.get("title", book.title)
            book.author = book_data.get("author", book.author)
            db.session.commit()
            return book
        return None

    # Define a method that deletes a book from the database
    @classmethod
    def delete_book(cls, book_id): 
        book = cls.get_book_by_id(book_id=book_id)
        if book: 
            db.session.delete(book)
            db.session.commit()
            return True
        return False
