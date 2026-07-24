from marshmallow import fields

from extensions import ma
from models.book import Book
from schemas.author_schema import AuthorSchema
from schemas.tag_schema import TagSchema


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True  # Optional: If you want to deserialize to model instances
        include_fk = True     # also expose author_id (foreign keys are hidden by default)

    # RELATIONSHIPS ARE NOT AUTOMATIC.
    # SQLAlchemyAutoSchema generates a field for every COLUMN it finds, but it
    # leaves relationships alone — it can't guess how deep you want to go, and
    # blindly following them could serialize half your database.
    #
    # fields.Pluck says: "use that schema, but give me only ONE field from it."
    # So instead of  "author": {"id": 1, "name": "Frank Herbert"}
    # we get         "author": "Frank Herbert"
    #
    # Swap Pluck for fields.Nested(AuthorSchema) if you'd rather have the whole
    # author object in the response.
    author = fields.Pluck(AuthorSchema, "name", dump_only=True)
    tags = fields.Pluck(TagSchema, "name", many=True, dump_only=True)


book_schema = BookSchema()
books_schema = BookSchema(many=True)  # For serializing multiple books
