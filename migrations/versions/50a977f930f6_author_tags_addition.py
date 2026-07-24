"""Author  & tags addition

Revision ID: 50a977f930f6
Revises: 983756e7202f
Create Date: 2026-07-24 09:34:39.038764

NOTE FOR STUDENTS
-----------------
Alembic auto-generated this file, but autogenerate can only see the SHAPE of the
schema — it knows nothing about the data already sitting in your tables. Three
things had to be fixed by hand:

  1. `create_foreign_key(None, ...)` -> constraints need a NAME on SQLite,
     because batch mode rebuilds the whole table and writes the constraint
     inline in CREATE TABLE. An unnamed constraint raises
     "ValueError: Constraint must have a name".

  2. `add_column(..., nullable=False)` on a table that already has rows is
     impossible — what value would the existing rows get? We add the column as
     NULLABLE, fill it in, and only then tighten it to NOT NULL.

  3. `drop_column('author')` would have thrown away every author name. We first
     copy those names into the new `authors` table (a DATA MIGRATION), then drop
     the old column.

This is exactly why the README says: always READ a generated migration before
running it.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50a977f930f6'
down_revision = '983756e7202f'
branch_labels = None
depends_on = None


def upgrade():
    # --- 1. The new `authors` table (must exist before books can point at it) ---
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # --- 2. Add author_id as NULLABLE for now ---
    # The books table already has rows. A NOT NULL column with no default has no
    # legal value for them, so we start permissive and tighten in step 4.
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))

    # --- 3. DATA MIGRATION: move author names out of `books` into `authors` ---
    # Every distinct name in books.author becomes one row in authors...
    op.execute(
        "INSERT INTO authors (name) "
        "SELECT DISTINCT author FROM books WHERE author IS NOT NULL"
    )
    # ...then each book is pointed at the matching author row.
    op.execute(
        "UPDATE books SET author_id = "
        "(SELECT id FROM authors WHERE authors.name = books.author)"
    )

    # --- 4. Now every row HAS an author_id, so the constraints can go on ---
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.alter_column('author_id', existing_type=sa.Integer(), nullable=False)
        batch_op.create_foreign_key(
            'fk_books_author_id_authors',   # <- the name autogenerate left as None
            'authors', ['author_id'], ['id']
        )
        batch_op.drop_column('author')      # safe now — the data lives in `authors`

    # --- 5. Tags + the many-to-many association table ---
    # Created last, so that rebuilding `books` in step 4 never happens while
    # book_tags is holding a foreign key to it.
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'book_tags',
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], name='fk_book_tags_book_id_books'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='fk_book_tags_tag_id_tags'),
        sa.PrimaryKeyConstraint('book_id', 'tag_id')
    )


def downgrade():
    # A good downgrade is the mirror image — including the data move.
    op.drop_table('book_tags')
    op.drop_table('tags')

    # Put the plain `author` text column back, nullable at first...
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=100), nullable=True))

    # ...copy the names back out of `authors`...
    op.execute(
        "UPDATE books SET author = "
        "(SELECT name FROM authors WHERE authors.id = books.author_id)"
    )

    # ...then tighten it and remove the relationship column.
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.alter_column('author', existing_type=sa.VARCHAR(length=100), nullable=False)
        batch_op.drop_constraint('fk_books_author_id_authors', type_='foreignkey')
        batch_op.drop_column('author_id')

    op.drop_table('authors')
