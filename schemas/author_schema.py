from extensions import ma
from models.author import Author


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True  # deserialize straight back into an Author object


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)  # For serializing multiple authors
