from datetime import datetime
from flask_blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): # This is a table called 'User', then we create coloumns within it
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) # Username must not be longer that 20characters, it has to be unique, it cannot be 'null' meaning it must not be empty
    email = db.Column(db.String(120), unique=True, nullable=False) # Email must not be longer that 120characters, it has to be unique, it cannot be 'null' meaning it must not be empty
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # This is the user profile picture. It is going to be stored as an harsh, and the harsh will be 20characters long. It must not be empty, Default profile picture that every user starts out with must be default
    password = db.Column(db.String(60), nullable=False) # The password will be stored has an harsh, the harsh will be 60characters long
    post = db.relationship('Post', backref='author', lazy=True) # This is to say the 'post' attribute has a relationship with the 'Post' module. The 'backref' is similar to adding another column to the Post module. What the backref allows us to do is When we have a post we can simply use the "author" attribute to get the user who created the post
    # Lazy describes when SQLAlchemy loads the data from the database. 'True' means SQLAlchemy will load the data as necessary in one go

    def __rep__(self): # To set what we want to return when we print a user object
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model): # This will hold our post
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) # Title length will max out at 100characters
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # data posted will have a 'column type' of datatime, it must not be empty, then the default will be set with the datetime.utcnow function without the brakets'()' because we are not calling it now, its just a argument. 'utc' is the most accurate time to use in a db
    content = db.Column(db.Text, nullable=False) # The type of this column is a txt, it must not be empty
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __rep__(self): # To set what we want to return when we print a post object
        return f"User('{self.title}', '{self.date_posted}')"
