from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture, send_reset_email


user = Blueprint('users', __name__)

@user.route("/register", methods=['GET', 'POST']) # For get and post request
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit(): # When you click on submit button in registeration
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                     password=hashed_password) # Storing user info into user class
        db.session.add(user) # About to add user to the database
        db.session.commit() # Push user to database
        # sends a message to affirm that user account have been created
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login')) # Takes user to login page
    return render_template('register.html', title='Register', form=form)


@user.route("/login", methods=['GET', 'POST']) # For get and post request
def login():
    if current_user.is_authenticated: # This is to check if user is logged in. if true, then when user clicks on register, it redirects to home
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit(): # After clicking on the submit button, check if the email, and password is equal to the admin, else you cannot login for now
        user = User.query.filter_by(email=form.email.data).first()
        # Checks if email doesnt exist before, and if password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # After logging in, it returns back to the present page before logging in
            next_page = request.args.get('next')
            # sends a message to affirm that user account have been created
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@user.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():  # After clicking on the submit button and nothing goes wrong, then update username and email to the newly inputed data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() # Update user info in the database
        flash('Your account has been updated!', 'success')
        # including this is to avoid resubmition when page is reloaded
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # This will populate the username and email field when the 'account' page is loaded
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@user.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    # this is to get all the posts that the username clicked has uploaded on the webpage
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)  # The order_by(Post.date_posted.desc()) is added to make sure that the latest post is found at the top of the blog. back slash is for breaking the line to write in the next line
    return render_template('user_posts.html', posts=posts, user=user)

@user.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated: # This is to check if user is logged in. if true, then when user clicks on register, it redirects to home
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit(): # After submitting the reset request, send an email message to the users email on how to reset there password
        user = User.query.filter_by(email=form.email.data).first()  # Fetch user email
        send_reset_email(user)  # Send mail to user email
        # Show user confirmation that the message has been sent to their mail
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login')) # Redirects user to the login page
    return render_template('reset_request.html', title='Reset Password', form=form)


@user.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:  # This is to check if user is logged in. if true, then when user clicks on register, it redirects to home
        return redirect(url_for('main.home'))
    # This gets the user's id from 'models.py'
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():  # When you click on submit button in registration
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()# Push user to database
        # sends a message to affirm that user account have been created
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login')) # Takes user to login page
    return render_template('reset_token.html', title='Reset Password', form=form)