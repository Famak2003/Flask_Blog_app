from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) #Module name
app.config['SECRET_KEY'] = 'b0a43574e67c9a9b73fef56717ca837e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app) # Initiating the data base object
bcrypt = Bcrypt(app) # Initiating the bcrypt object
login_manager = LoginManager(app)# Initiating the LoginManager object
login_manager.login_view = 'login' # The view is the function name of our route. This is also to restrict access to the account page if user is not logged in
login_manager.login_message_category = 'info' # This is to style the "Please log in to access this page" message
app.app_context().push() # always remember to add this to your init file.....if not the 'db.create_all()' wont work......it needs an active flask file to work, "app.app_content().push()" tells the db where to look for its requested files

from flask_blog import route