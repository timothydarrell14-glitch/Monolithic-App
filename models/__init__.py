# This file makes `models/` a package — and gives it one important job:
# it is the SINGLE PLACE that imports every model.
#
# WHY THIS MATTERS
# ----------------
# Our models refer to each other by STRING name, e.g. in models/book.py:
#
#     author = db.relationship('Author', back_populates='books')
#     tags   = db.relationship('Tag', secondary='book_tags', ...)
#
# SQLAlchemy doesn't resolve those strings straight away. It looks them up later,
# in a registry that each class adds itself to WHEN ITS FILE IS IMPORTED.
#
# So if something inspects the Book mapper before models/author.py has ever been
# imported, the lookup fails with:
#
#     InvalidRequestError: expression 'Author' failed to locate a name ('Author')
#
# Importing them all here means one `from models import ...` guarantees every
# model and association table is registered — no import-order landmines.
#
# The association table comes first because the relationships reference it.
from models.associations import book_tags
from models.author import Author
from models.book import Book
from models.tag import Tag
from models.user import User

# __all__ documents the public surface of this package.
__all__ = ["book_tags", "Author", "Book", "Tag", "User"]
