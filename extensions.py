from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

# create an instance of the class SQLAlchemy
# Object Relational Mapper (ORM) that allows you to interact with the database using Python objects instead of writing raw SQL queries.
db = SQLAlchemy()
ma = Marshmallow() # create an instance of the class Marshmallow
jwt = JWTManager() # create an instance of the class JWTManager