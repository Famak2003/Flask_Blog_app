from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config




bcrypt = Bcrypt()  # Initiating the bcrypt object
login_manager = LoginManager()  # Initiating the LoginManager object
# The view is the function name of our route. This is also to restrict access to the account page if user is not logged in
login_manager.login_view = 'user.login'
# This is to style the "Please log in to access this page" message
login_manager.login_message_category = 'info'
db = SQLAlchemy()  # Initiating the data base object


mail = Mail()

# from flask_blog.models import User, Post



def create_app(config_class = Config):
    app = Flask(__name__)  # Module name
    app.config.from_object(Config)

    mail.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    from flask_blog.users.routes import user
    from flask_blog.main.routes import main
    from flask_blog.posts.routes import posts
    from flask_blog.errors.handlers import errors

    app.register_blueprint(user)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.app_context().push()  # always remember to add this to your init file.....if not the 'db.create_all()' wont work......it needs an active flask file to work, "app.app_content().push()" tells the db where to look for its requested files

    return app