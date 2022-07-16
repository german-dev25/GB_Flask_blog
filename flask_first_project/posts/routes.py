from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flask_first_project import db
from flask_first_project.models import Post, Comment, Category
from flask_first_project.posts.forms import PostForm, CommentForm
from flask_first_project.posts.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if request.method == "POST":
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
        else:
            picture_name = 'default.jpg'
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
            category_id=form.category.data,
            image_file=picture_name,
        )
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',
                           title='Новый пост',
                           form=form,
                           legend='Новый пост',
                           image_file=form.picture.data,
                           )


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            post_id=post_id,
            username=current_user.username,
        )
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен', 'success')
        return redirect(f'/post/{post_id}')
    return render_template('full_post.html', title=post.title, post=post, form=form, legend='Оставить комментарий')


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.category.data
        if form.picture.data:
            post.image_file = save_picture(form.picture.data)
        db.session.commit()
        flash('Ваш пост обновлен!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        image_file = url_for('static', filename='posts_pics/' + post.image_file)
    return render_template('create_post.html', title='Редактирование поста', image_file=image_file, form=form, legend='Редактирование поста')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/post/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)


@posts.context_processor
def context_date():
    categories = Category.query.all()
    some_last_post = Post.query.all()
    return dict(
        some_last_post=some_last_post,
        categories=categories,
    )
