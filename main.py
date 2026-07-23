from flask import Flask, json, jsonify, request
from extensions import db, ma, jwt
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from controllers.book_controller import BookController
from controllers.user_controller import AuthController
from schemas.book_schema import book_schema, books_schema
from schemas.user_schema import user_schema, users_schema

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

from models.book import Book
from models.user import User

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

@app.route('/about')
def about():
    return jsonify({"message": "This is a simple Book API built with Flask."})

if __name__ == '__main__':
    app.run(debug=True)