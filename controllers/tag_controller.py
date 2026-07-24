# this is where we will define the logic for handling tag-related requests - controller layer
from models.tag import Tag
from extensions import db

class TagController:
    # Define a method to get all tags from the database
    @classmethod
    def get_all_tags(cls):
        "SELECT * FROM tags"
        return Tag.query.all()

    # Define a method that retrieves a single tag by its ID
    @classmethod
    def get_tag_by_id(cls, tag_id):
        "SELECT * FROM tags WHERE id = :tag_id"
        return Tag.query.filter_by(id=tag_id).first()

    # Define a method that finds a tag by its name (used to spot duplicates)
    @classmethod
    def get_tag_by_name(cls, name):
        "SELECT * FROM tags WHERE name = :name"
        return Tag.query.filter_by(name=name).first()

    # Define a method that creates a new tag in the database
    @classmethod
    def create_tag(cls, tag_data):
        "INSERT INTO tags (name) VALUES (:name)"
        # `name` is declared unique=True on the model, so the DATABASE would
        # reject a duplicate with an IntegrityError — which Flask turns into an
        # ugly 500. We check first so the route can return a clean 409 instead.
        # Rule of thumb: the database is your safety net, not your error message.
        if cls.get_tag_by_name(tag_data["name"]):
            return None

        new_tag = Tag(name=tag_data["name"])
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

    # Define a method that updates a tag's name
    @classmethod
    def update_tag(cls, tag_id, tag_data):
        tag = cls.get_tag_by_id(tag_id=tag_id)
        if tag:
            tag.name = tag_data.get("name", tag.name)
            db.session.commit()
            return tag
        return None

    # Define a method that deletes a tag from the database
    @classmethod
    def delete_tag(cls, tag_id):
        # Unlike authors, deleting a tag is SAFE for the books. There's no
        # cascade here — SQLAlchemy just removes the matching rows from the
        # book_tags association table, and the books themselves are untouched.
        tag = cls.get_tag_by_id(tag_id=tag_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return True
        return False

    # Define a method that returns every book carrying one tag.
    # Walking the many-to-many in the other direction — `tag.books` hides the
    # JOIN through book_tags entirely.
    @classmethod
    def get_books_for_tag(cls, tag_id):
        "SELECT b.* FROM books b JOIN book_tags bt ON bt.book_id = b.id WHERE bt.tag_id = :tag_id"
        tag = cls.get_tag_by_id(tag_id=tag_id)
        if tag:
            return tag.books
        return None
