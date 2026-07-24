from extensions import db

# The ASSOCIATION TABLE for the many-to-many relationship between books and tags.
#
# A many-to-many can't be stored with a foreign key on either side (a book has many
# tags AND a tag has many books), so we need a third table that holds nothing but
# the pairings:
#
#   book_id | tag_id
#   --------+--------
#      1    |   3      -> "Dune" is tagged "sci-fi"
#      1    |   7      -> "Dune" is also tagged "classic"
#      2    |   3      -> "Neuromancer" is also "sci-fi"
#
# Note this is a db.Table, NOT a db.Model — it has no id and no Python class,
# because it's pure plumbing. We never query it directly; SQLAlchemy uses it
# behind the scenes via `secondary="book_tags"` on both sides.
#
# db.Table's signature is Table(name, *columns) — the FIRST argument is the table
# name, and everything after it must be a Column or a Constraint.
book_tags = db.Table(
    'book_tags',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)
