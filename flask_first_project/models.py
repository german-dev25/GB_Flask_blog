from datetime import datetime
from random import random

from flask_first_project import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    username = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
    )
    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.png',
    )
    password = db.Column(
        db.String(60),
        nullable=False,
    )
    comments = db.relationship(
        'Comment',
        backref='author',
        lazy=True,
    )
    posts = db.relationship(
        'Post',
        backref='author',
        lazy=True,
    )
    liked_posts = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user',
        lazy='dynamic',
    )

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0


class Post(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    title = db.Column(
        db.String(100),
        nullable=False,
    )
    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    content = db.Column(
        db.Text,
        nullable=False,
    )
    image_file = db.Column(
        db.String(20),
        nullable=False,
        default='default.png',
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )
    category_id = db.Column(
        db.Integer(),
        db.ForeignKey('category.id'),
        nullable=True,
        default='Без Категории'
    )
    likes = db.relationship(
        'PostLike',
        backref='post',
        lazy='dynamic'
    )


class Category(db.Model):
    id = db.Column(
        db.Integer(),
        primary_key=True,
    )
    category = db.Column(
        db.String(20),
        nullable=False,
        default='None',
    )
    slug = db.Column(
        db.String(20),
        nullable=False,
        default='None',
    )
    posts = db.relationship(
        'Post',
        backref='category',
    )
    color = db.Column(
        db.String(10),
        nullable=False,
        default='000000'
    )

    def __repr__(self):
        return "<{}>".format(self.category)


class Comment(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    body = db.Column(
        db.String(200),
        nullable=False,
    )
    add_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
        nullable=False,
    )
    username = db.Column(
        db.Integer,
        db.ForeignKey('user.username'),
        nullable=False,
    )


class PostLike(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id'),
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
    )
