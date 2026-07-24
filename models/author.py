from extensions import db

class Author(db.Model): 
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    books = db.relationship('Book', back_populates="author", cascade="all, delete-orphan")  # Establish a relationship with the Book model

    def __repr__(self): # Define the string representation of the Author object for debugging purposes
        return f"<Author {self.name}>"


