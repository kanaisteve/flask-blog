from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import db, User, Post, Note, Comment, Like
import json

views = Blueprint('views', __name__)

# home page
@views.route('/')
@views.route('/home')
def home():
    return render_template('index.html')

# about page
@views.route('/about')
def about():
    return render_template('about.html')

# services page
@views.route('/services')
def services():
    return render_template('services.html')

# display blog posts
@views.route('/posts')
def blog_posts():
    posts = Post.query.all()
    return render_template('blog/posts.html', posts=posts)

# single post
@views.route('/posts/<string:id>')
def get_single_post(id):
    post = Post.query.filter_by(id=id).first()
    return render_template('blog/post.html', post=post)

# get author posts
@views.route('/posts/<username>')
@login_required
def author(username):
    user = User.query.filter_by(username=username).first()

    # check if user exists
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    # get all posts by user
    # posts = Post.query.filter_by(author_id=user.id).all() # delete this cz it's expensive. we will have to make a new query to the db
    posts = user.posts

    return render_template('blog/author.html', posts=posts, username=username)

# post comment
@views.route('/create-comment/<post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    comment = request.form.get('comment')

    if not comment:
        flash('Comment cannot be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(content=comment, post_id=post_id, author_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist', category='error')

    return redirect(url_for('views.blog_posts'))

# delete comment
@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author_id and current_user.id != comment.post.author_id:
        flash('You do no have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.blog_posts'))

# like post
@views.route('/like-post/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author_id=current_user.id, post_id=post_id).first()

    if not post:
        # flash('Post does not exis.', category='error')
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    # return redirect(url_for('views.blog_posts'))
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})


# delete post
@views.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', category='success')
    
    return redirect(url_for('views.blog_posts'))

# dashboard view
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('home.html')

# create post route
@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not content:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(title=title, content=content, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog_posts'))

    return render_template('posts/create_post.html')

# Display All Notes
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    notes = Note.query.all()

    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(content=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('notes/index.html', notes=notes)

# delete note
@views.route('/delete-note/<int:id>')
@login_required
def delete_note(id):
    # note = json.loads(request.data)
    #  noteId = note['note']
    # note = Note.query.get(id)
    note = Note.query.filter_by(id=id).first()

    if not note:
        flash("Note does not exist.", category='error')
    elif current_user.id != note.user_id:
        flash('You do not have permission to delete this note.', category='error')
    else:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted successfully', category='success')
    
    return redirect(url_for('views.notes'))
    
    # return jsonify({})
