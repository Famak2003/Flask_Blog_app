from flask import render_template, request, Blueprint
from flask_blog.models import Post


main = Blueprint('main', __name__)

# This forward slash(/) is the root page or the home page of this webapp
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    # The order_by(Post.date_posted.desc()) is added to make sure that the latest post is found at the top of the blog. The pageinate is to limit the number of posts loaded per page, therefore numbers of how many post should be available per page is inserted into it, and the reset of the unloaded page will be in the next on at the footer of the blog
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')