from extensions import db

classModel = db.Model

# Define the Book model - Inherit from db.Model to create a database model for the Book entity
class Book(classModel): 

    __tablename__ = "books" # Specify the table name in the database

    id = db.Column(db.Integer, primary_key=True) # Define the 'id' column as an integer and set it as the primary key
    title = db.Column(db.String(100), nullable=False) # Define the 'title' column as a string with a maximum length of 100 characters and set it as not nullable
    author = db.Column(db.String(100), nullable=False) # Define the 'author' column as a string with a maximum length of 100 characters and set it as not nullable

    def  __repr__(self): # Define the string representation of the Book object for debugging purposes
        return f"<Book {self.title} by {self.author}>"

    def to_dict(self):
        # Serialize this Book object into a plain dictionary.
        # jsonify() can only convert basic types (dict/list/str/int...),
        # NOT a custom Book object — so we translate here, in one place.
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
        }