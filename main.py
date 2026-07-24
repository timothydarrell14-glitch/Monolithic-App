from flask import Flask, jsonify, request
from extensions import db, ma, jwt
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# IMPORT ORDER MATTERS HERE — models BEFORE schemas.
# A Marshmallow SQLAlchemyAutoSchema inspects its model the moment the schema
# class is created, which forces SQLAlchemy to resolve every string-based
# relationship ('Author', 'Tag', 'book_tags'). If those classes haven't been
# imported yet, you get:
#   InvalidRequestError: expression 'Author' failed to locate a name ('Author')
# Importing the models package first registers all of them in one line.
from models import Book, User, Author, Tag

from controllers.book_controller import BookController
from controllers.user_controller import AuthController
from controllers.author_controller import AuthorController
from controllers.tag_controller import TagController
from schemas.book_schema import book_schema, books_schema
from schemas.user_schema import user_schema, users_schema
from schemas.author_schema import author_schema, authors_schema
from schemas.tag_schema import tag_schema, tags_schema

app = Flask(__name__)
# Configure the database URI (replace with your actual database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key in production

# Initialize the database with the Flask app
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)


# initialize Flask-Migrate with the app and database
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Book API!"})

##################### USER AUTHENTICATION ROUTES #####################

@app.route('/register', methods=['POST'])
def register():

    user_data = request.json
    new_user = AuthController.register_user(user_data=user_data)

    if new_user:
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"error": "User registration failed"}), 400
    

@app.route('/login', methods=['POST'])
def login(): 

    data = request.json
    user = AuthController.authenticate_user(username=data.get("username"), password=data.get("password"))

    if user:

        token = create_access_token(identity=str(user.id), additional_claims={
            "username": user.username,
            "email": user.email,
            "id": user.id
        })

        return jsonify({"message": "Login successful", "token": token}), 200
    return jsonify({"error": "Invalid username or password"}), 401

############################ BOOK ROUTES #####################

@app.route('/books')
@jwt_required()
def get_books():
    books = BookController.get_all_books()
    return jsonify(books_schema.dump(books))


@app.route('/books/<int:book_id>')
@jwt_required()
def get_book(book_id):
    book = BookController.get_book_by_id(book_id)
    if book:
        return jsonify(book_schema.dump(book))
    return jsonify({"error": "Book not found"}), 404

@app.route('/books', methods=['POST'])
@jwt_required()
def create_book():
    new_book = BookController.create_book(request.json)
    return jsonify(book_schema.dump(new_book)), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    # The controller already applies defaults for any missing fields,
    # so we can hand it the raw JSON body directly.
    updated_book = BookController.update_book(book_id, request.json)

    if updated_book:
        return jsonify(book_schema.dump(updated_book)), 200

    return jsonify({"error": "Book not found"}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    book = BookController.get_book_by_id(book_id)

    if book: 
        BookController.delete_book(book_id)
        return jsonify({"message": "Book deleted successfully"}), 204
    else: 
        return jsonify({"error": "Book not found"}), 404

############################ AUTHOR ROUTES #####################

@app.route('/authors')
@jwt_required()
def get_authors():
    authors = AuthorController.get_all_authors()
    return jsonify(authors_schema.dump(authors))

@app.route('/authors/<int:author_id>')
@jwt_required()
def get_author(author_id):
    author = AuthorController.get_author_by_id(author_id)

    if author:
        return jsonify(author_schema.dump(author)), 200

    return jsonify({"error": "Author not found"}), 404

@app.route('/authors', methods=['POST'])
@jwt_required()
def create_author():
    new_author = AuthorController.create_author(request.json)
    return jsonify(author_schema.dump(new_author)), 201

@app.route('/authors/<int:author_id>', methods=['PUT'])
@jwt_required()
def update_author(author_id):
    updated_author = AuthorController.update_author(author_id, request.json)

    if updated_author:
        return jsonify(author_schema.dump(updated_author)), 200

    return jsonify({"error": "Author not found"}), 404

@app.route('/authors/<int:author_id>', methods=['DELETE'])
@jwt_required()
def delete_author(author_id):
    # ⚠️ Remember the cascade: this deletes the author AND all their books.
    if AuthorController.delete_author(author_id):
        return jsonify({"message": "Author deleted successfully"}), 204

    return jsonify({"error": "Author not found"}), 404

@app.route('/authors/<int:author_id>/books')
@jwt_required()
def get_author_books(author_id):
    # A NESTED route: "the books belonging to THIS author."
    # Reading the URL left to right tells you the relationship.
    books = AuthorController.get_books_for_author(author_id)

    # `is None` matters here — an author with zero books returns an empty
    # list, and `if not books` would wrongly call that a 404.
    if books is None:
        return jsonify({"error": "Author not found"}), 404

    return jsonify(books_schema.dump(books)), 200

############################ TAG ROUTES #####################

@app.route('/tags')
@jwt_required()
def get_tags():
    tags = TagController.get_all_tags()
    return jsonify(tags_schema.dump(tags))

@app.route('/tags/<int:tag_id>')
@jwt_required()
def get_tag(tag_id):
    tag = TagController.get_tag_by_id(tag_id)

    if tag:
        return jsonify(tag_schema.dump(tag)), 200

    return jsonify({"error": "Tag not found"}), 404

@app.route('/tags', methods=['POST'])
@jwt_required()
def create_tag():
    new_tag = TagController.create_tag(request.json)

    # The controller returns None when the name is already taken.
    # 409 CONFLICT is the right status code — the request was well-formed,
    # it just clashes with the current state of the server.
    if new_tag is None:
        return jsonify({"error": "A tag with that name already exists"}), 409

    return jsonify(tag_schema.dump(new_tag)), 201

@app.route('/tags/<int:tag_id>', methods=['PUT'])
@jwt_required()
def update_tag(tag_id):
    updated_tag = TagController.update_tag(tag_id, request.json)

    if updated_tag:
        return jsonify(tag_schema.dump(updated_tag)), 200

    return jsonify({"error": "Tag not found"}), 404

@app.route('/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_id):
    # Safe: only the book_tags pairings go away, never the books themselves.
    if TagController.delete_tag(tag_id):
        return jsonify({"message": "Tag deleted successfully"}), 204

    return jsonify({"error": "Tag not found"}), 404

@app.route('/tags/<int:tag_id>/books')
@jwt_required()
def get_tag_books(tag_id):
    # The many-to-many, walked in the other direction.
    books = TagController.get_books_for_tag(tag_id)

    if books is None:
        return jsonify({"error": "Tag not found"}), 404

    return jsonify(books_schema.dump(books)), 200

@app.route('/about')
def about():
    return jsonify({"message": "This is a simple Book API built with Flask."})

if __name__ == '__main__':
    app.run(debug=True)