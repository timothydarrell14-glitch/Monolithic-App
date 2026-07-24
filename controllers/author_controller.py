# this is where we will define the logic for handling author-related requests - controller layer
from models.author import Author
from extensions import db

class AuthorController:
    # Define a method to get all authors from the database
    @classmethod
    def get_all_authors(cls):
        "SELECT * FROM authors"
        return Author.query.all()

    # Define a method that retrieves a single author by their ID
    @classmethod
    def get_author_by_id(cls, author_id):
        "SELECT * FROM authors WHERE id = :author_id"
        return Author.query.filter_by(id=author_id).first()

    # Define a method that creates a new author in the database
    @classmethod
    def create_author(cls, author_data):
        "INSERT INTO authors (name) VALUES (:name)"
        new_author = Author(name=author_data["name"])
        db.session.add(new_author)
        db.session.commit()
        return new_author

    # Define a method that updates an author's information
    @classmethod
    def update_author(cls, author_id, author_data):
        author = cls.get_author_by_id(author_id=author_id)
        if author:
            author.name = author_data.get("name", author.name)
            db.session.commit()
            return author
        return None

    # Define a method that deletes an author from the database
    @classmethod
    def delete_author(cls, author_id):
        # ⚠️ HEADS UP: models/author.py declares the books relationship with
        #    cascade="all, delete-orphan"
        # That means deleting an author ALSO DELETES EVERY BOOK they wrote.
        # It's a deliberate choice (a book can't exist without its author here),
        # but it's the kind of thing that surprises people in production.
        # Use get_books_for_author() first if you want to warn the caller.
        author = cls.get_author_by_id(author_id=author_id)
        if author:
            db.session.delete(author)
            db.session.commit()
            return True
        return False

    # Define a method that returns every book written by one author.
    # This is the payoff of the relationship: no manual JOIN, no second query
    # written by hand — `author.books` just works, because back_populates
    # wired the two models together.
    @classmethod
    def get_books_for_author(cls, author_id):
        "SELECT * FROM books WHERE author_id = :author_id"
        author = cls.get_author_by_id(author_id=author_id)
        if author:
            return author.books
        return None
