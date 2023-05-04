import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required




@app.route("/") # This forward slash(/) is the root page or the home page of this webapp
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # The order_by(Post.date_posted.desc()) is added to make sure that the latest post is found at the top of the blog. The pageinate is to limit the number of posts loaded per page, therefore numbers of how many post should be available per page is inserted into it, and the reset of the unloaded page will be in the next on at the footer of the blog
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST']) # For get and post request
def register():
    if current_user.is_authenticated: 
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit(): # When you click on submit button in registeration
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # Storing user info into user class
        db.session.add(user) # About to add user to the database
        db.session.commit() # Push user to database
        flash(f'Your account has been created! You are now logged in', 'success') # sends a message to affirm that user account have been created
        return redirect(url_for('login')) # Takes user to login page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST']) # For get and post request
def login():
    if current_user.is_authenticated: # This is to check if user is logged in. if true, then when user clicks on register, it redirects to home
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit(): # After clicking on the submit button, check if the email, and password is equal to the admin, else you cannot login for now
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): # Checks if email doesnt exist before, and if password is correct
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # After logging in, it returns back to the present page before logging in
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # Generates a random name for the image
    _, f_ext = os.path.splitext(form_picture.filename) # This returns two values....It returns the file name without the extension e.g(pelumi), and returns the extension its self e.g(jpg)////// '_' means when you dont need the variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # "app.root_path" is the root path of this application all the way up to the package directory.....So what this line is doing is creating a path for the picture by joining all of them together

    # We resize the image to 125 X 125 before saving it
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) # Here, we save the picture to the created path

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit(): # After clicking on the submit button and nothing goes wrong, then update username and email to the newly inputed data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() # Update user info in the database
        flash('Your account has been updated succefully!', 'success')
        return redirect(url_for('account')) # including this is to avoid resubmition when page is reloaded
    elif request.method == 'GET': # This will populate the username and email field when the 'account' page is loaded
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required # Login is rrequired for this page to be accessable
def new_post():
    form = PostForm()
    if form.validate_on_submit(): # After clicking on the submit button and nothing goes wrong, then update Post to the database
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # Creating Post Table in the database
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>") # Here, it create a rouute based on the unique id each post has
def post(post_id): # It takes post_id as an input
    post = Post.query.get_or_404(post_id) # This gets the content that exist at the id.....if nothing exist there, it return 404 (Page not found)
    return render_template('post.html', title=post.title, post=post)
    

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # If post_id isnt found, it returns 404 error
    if post.author != current_user: # This is to ensure that only the author can edit their post
        abort(403) # This is the http response for a forbidden route
    form = PostForm()
    if form.validate_on_submit(): # When User clicks on the submit button, It update the post content to the new content user inputed
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # Here no need to add before commiting, because its already in the database, we are just updating it
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': # If its a get request, it populate the title and content with the current post
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # This is to ensure that only the author can edit their post
        abort(403) # This is the http response for a forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404() # this is to get all the posts that the username clicked has uploaded on the webpage
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # The order_by(Post.date_posted.desc()) is added to make sure that the latest post is found at the top of the blog. back slash is for breaking the line to write in the next line
    return render_template('user_posts.html', posts=posts, user=user)
