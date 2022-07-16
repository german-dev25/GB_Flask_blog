from flask import render_template, Blueprint, request
from flask_first_project.models import User, Post, Category, PostLike, Comment

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    all_posts = Post.query.order_by(Post.date_posted.desc())
    posts = all_posts.paginate(page=page, per_page=8)
    return render_template(
        'home.html',
        posts=posts,
        title='Все посты',
        legend='6')


@main.route("/home/<int:cat_id>")
def home_category(cat_id):
    page = request.args.get('page', 1, type=int)
    post_by_category = Post.query \
        .filter_by(category_id=cat_id) \
        .paginate(page=page, per_page=8)
    return render_template(
        'home.html',
        posts=post_by_category,
        page=page,
        legend=6
    )


@main.context_processor
def context_date():
    categories = Category.query.all()
    some_last_post = Post.query.all()
    last_comments = Comment.query.order_by(Comment.add_time)
    return dict(
        some_last_post=some_last_post,
        categories=categories,
        last_comments=last_comments,
    )
