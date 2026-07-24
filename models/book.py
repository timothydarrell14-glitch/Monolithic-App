from extensions import db

classModel = db.Model

# Define the Book model - Inherit from db.Model to create a database model for the Book entity
class Book(classModel): 

    __tablename__ = "books" # Specify the table name in the database

    id = db.Column(db.Integer, primary_key=True) # Define the 'id' column as an integer and set it as the primary key
    title = db.Column(db.String(100), nullable=False) # Define the 'title' column as a string with a maximum length of 100 characters and set it as not nullable

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False) # Define the 'author_id' column as an integer and set it as a foreign key referencing the 'id' column in the 'authors' table
    author = db.relationship('Author', back_populates='books') # Define a relationship to the Author model, allowing access to the associated author of the book

    tags = db.relationship('Tag', secondary="book_tags", back_populates="books") # Define a many-to-many relationship with the Tag model through the 'book_tags' association table

    def  __repr__(self): # Define the string representation of the Book object for debugging purposes
        # self.author is an Author OBJECT now, so reach in for the readable name
        return f"<Book {self.title} by {self.author.name if self.author else 'Unknown'}>"

    def to_dict(self):
        # Serialize this Book object into a plain dictionary.
        # jsonify() can only convert basic types (dict/list/str/int...),
        # NOT a custom Book object — so we translate here, in one place.
        #
        # NOTE: `self.author` is no longer a string! It's now a relationship,
        # so it hands back a whole Author OBJECT — which jsonify can't serialize
        # either. We reach into it for the plain value we actually want.
        # Same for `self.tags`, which is a list of Tag objects.
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author.name if self.author else None,
            "tags": [tag.name for tag in self.tags],
        }