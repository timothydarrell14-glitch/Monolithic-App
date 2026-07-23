from extensions import ma 
from models.book import Book 

class BookSchema(ma.SQLAlchemyAutoSchema): 
    class Meta: 
        model = Book 
        load_instance = True # Optional: If you want to deserialize to model instances

book_schema = BookSchema()
books_schema = BookSchema(many=True) # For serializing multiple books