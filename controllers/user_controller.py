from models.user import User 
from extensions import db

class AuthController:

    @classmethod
    def register_user(cls, user_data):
        new_user = User(username=user_data["username"], email=user_data["email"]) # user object to be added to db
        new_user.set_password(user_data["password"]) # hash the password and set it to the user object
        db.session.add(new_user) # add the user object to the session
        db.session.commit() # commit the session to the database
        return new_user
    
    @classmethod
    def authenticate_user(cls, username, password):
        user = User.query.filter_by(username=username).first() # get the user object from the database
        if user and user.check_password(password): # check if the user exists and the password is correct
            return user
        return None
    
    