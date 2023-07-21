
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
# from datetime import datetime

# Init db
db = SQLAlchemy()
DB_NAME = 'database.db'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    posts = db.relationship('Post', backref='author', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    notes = db.relationship('Note', backref='user', passive_deletes=True) # tell Flask and SQLAlchemy to add user's notes everytime a note is created. This relationship will be a list and will store all different notes.

    # def __repr__(self):
    #     return '<User %r>' % self.username
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

    # def __repr__(self):
    #     return '<Post %r>' % self.title

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return '<Category %r>' % self.name

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(10000))
    create_at = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # one to many relationship: a user can create many notes.

# Note:
# One User to Many Likes
# One User to Many Posts
# One Post to Many Comment
# One Post to Many Liks

# Future Features:
# ----------------
# 1. View Count
# 2. Bookmark
# 3. Comment and Replay