# this is where we will define the logic for handling book-related requests - controller layer
from models.book import Book
from models.author import Author
from models.tag import Tag
from extensions import db

class BookController:

    # ---------------------------------------------------------------- helpers
    # These two are the "find-or-create" pattern. The API still lets a client
    # send an author NAME ("Frank Herbert"), but the database now needs an
    # author ROW to point at. So we look the name up, and only insert a new
    # Author if we've never seen it before — otherwise every POST would create
    # a duplicate author.
    #
    # They're prefixed with _ to signal "internal helper, not part of the
    # controller's public API."
    @classmethod
    def _get_or_create_author(cls, name):
        "SELECT * FROM authors WHERE name = :name   (then INSERT if missing)"
        author = Author.query.filter_by(name=name).first()
        if author is None:
            author = Author(name=name)
            db.session.add(author)
        return author

    @classmethod
    def _get_or_create_tags(cls, names):
        "Same idea, but for a LIST of tag names -> a list of Tag objects"
        return [
            Tag.query.filter_by(name=name).first() or Tag(name=name)
            for name in names
        ]

    # ------------------------------------------------------------------ CRUD
    # Define a method to get all books from the database
    @classmethod
    def get_all_books(cls):
        "SELECT * FROM books"
        return Book.query.all()

    # Define a method that creates a new book in the database
    @classmethod
    def create_book(cls, book_data):
        "insert into books (title, author_id) values (:title, :author_id)"
        # `author=` now takes an Author OBJECT, not a string — SQLAlchemy fills
        # in author_id for us when the session is flushed.
        new_book = Book(
            title=book_data["title"],
            author=cls._get_or_create_author(book_data["author"]),
        )
        # tags are optional — a book with no tags is perfectly valid
        if book_data.get("tags"):
            new_book.tags = cls._get_or_create_tags(book_data["tags"])

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
            # only touch the relationships if the client actually sent them
            if "author" in book_data:
                book.author = cls._get_or_create_author(book_data["author"])
            if "tags" in book_data:
                book.tags = cls._get_or_create_tags(book_data["tags"])
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
