from flask import Flask, jsonify, request
from extensions import db
from flask_migrate import Migrate

app = Flask(__name__)
# Configure the database URI (replace with your actual database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# initialize Flask-Migrate with the app and database
migrate = Migrate(app, db)

from models.book import Book

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Book API!"})

@app.route('/books')
def get_books():
    return jsonify(books)

@app.route('/books/<int:book_id>')
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    return jsonify(book) if book else jsonify({"error": "Book not found"}), 404

@app.route('/books', methods=['POST'])
def create_book():
    new_book = {
        "id": len(books) + 1,
        "title": request.json.get("title"),
        "author": request.json.get("author")
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    book["title"] = request.json.get("title", book["title"])
    book["author"] = request.json.get("author", book["author"])
    return jsonify(book)

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Book deleted successfully"}), 204

@app.route('/about')
def about():
    return jsonify({"message": "This is a simple Book API built with Flask."})

if __name__ == '__main__':
    app.run(debug=True)