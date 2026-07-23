from extensions import db 
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model): 
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self): 
        return f"<User {self.username}>"
    
    # method to set a users password 
    def set_password(self, password): 
        # raw => JohnDoe123! => hashed => $2b$12$KIXQ1
        self.password = generate_password_hash(password)

    # method to check a users password
    def check_password(self, password):
        # raw => JohnDoe123! => hashed => $2b$12$KIXQ1
        # check_password_hash() will hash the raw password and compare it to the stored hashed password
        return check_password_hash(self.password, password)