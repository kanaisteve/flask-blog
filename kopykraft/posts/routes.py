from flask import render_template, flash, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from kopykraft.extensions import db
from flask import render_template
from kopykraft.posts import posts
from kopykraft.models import Posts
from webforms import PostForm, SearchForm

# Add Post Page
@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()

    if form.validate_on_submit():
        # get data from form
        title = form.title.data
        content = form.content.data
        slug = form.slug.data
        author_id = current_user.id

        # create new post
        post = Posts(title=title, content=content, slug=slug, author_id=author_id)

        # clear form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''

        # Add post data to db
        db.session.add(post)
        db.session.commit()

        # Return a flash message
        flash("Blog Post Submitted Sucessfully!")
        return redirect(url_for('posts.index'))
    
    # Return to the webpage
    return render_template("posts/create.html", form=form)

# Get All Blog Posts
@posts.route('/')
def index():
    # fetch all posts from database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts/index.html', posts=posts)

# Get Single Blog Post
@posts.route('/<int:id>')
def show(id):
    # fetch all posts from database
    post = Posts.query.get_or_404(id)
    return render_template('posts/show.html', post=post)

# Edit Blog Post
@posts.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()

    # handle post update
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        author_id = current_user.id

        # update database
        db.session.add(post)
        db.session.commit()
        flash('Post Update Successfully!')
        return redirect(url_for('posts.show', id=id))
    
    # check if current user is the author or admin(id:13) of the post
    if current_user.id == post.author.id or current_user.id == 13:
        form.title.data = post.title
        form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('posts/edit.html', post=post, form=form)
    else:
        flash('You are\'t authorized to edit this post...')
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts/index.html', posts=posts)


# Delete Blog Post
@posts.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Posts.query.get_or_404(id)
    author_id = current_user.id

    # get all post from database
    posts = Posts.query.order_by(Posts.date_posted)

    # only allow author or admin(id:13) of post to delete this post
    if author_id == post.author.id or author_id == 13:
        try:
            db.session.delete(post)
            db.session.commit()
            # return message
            flash('Blog Post Delete Successfully!')
            # get all post from database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts/index.html', posts=posts)
        except:
            # return error message
            flash('Whoops! There was a problem when deleting the blog post, try again...')
            return redirect(url_for('posts.index', posts=posts))
    else:
        # flash message to user
        flash('You Aren\'t Authorized to delete that post')
        return redirect(url_for('posts.index'))
    
# create search function
@posts.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query

    if form.validate_on_submit():
        search = form.search.data
        # query the database
        posts = posts.filter(Posts.content.like('%' + search + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template('posts/search_result.html', form=form, search=search, posts=posts)
    
