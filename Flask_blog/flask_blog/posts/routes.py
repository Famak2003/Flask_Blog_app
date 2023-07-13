
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm
posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required  # Login is rrequired for this page to be accessable
def new_post():
    form = PostForm()
    if form.validate_on_submit():  # After clicking on the submit button and nothing goes wrong, then update Post to the database
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  # Creating Post Table in the database
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


# Here, it create a rouute based on the unique id each post has
@posts.route("/post/<int:post_id>")
def post(post_id):# It takes post_id as an input
    # This gets the content that exist at the id.....if nothing exist there, it return 404 (Page not found)
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # If post_id isnt found, it returns 404 error
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:  # This is to ensure that only the author can edit their post
        abort(403)  # This is the http response for a forbidden route
    form = PostForm()
    if form.validate_on_submit():  # When User clicks on the submit button, It update the post content to the new content user inputed
        post.title = form.title.data
        post.content = form.content.data
        # Here no need to add before commiting, because its already in the database, we are just updating it
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET': # If its a get request, it populate the title and content with the current post
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:  # This is to ensure that only the author can edit their post
        abort(403)  # This is the http response for a forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))







