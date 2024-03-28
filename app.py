from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///biolgy_new'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
app.config['SQLALCHEMY_ECHO'] = True
toolbar = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def Home_Page():
    """Home page"""

    return redirect("/users")

@app.route('/users')
def all_users():
    """Show all users page."""
    users = User.query.all()
    return render_template('users/users.html',users=users)


@app.route('/users/<int:user_id>')
def profiles(user_id):
    """Show each user's profile."""
    user_profile = User.query.get_or_404(user_id)
    user_posts = user_profile.posts 
    return render_template('users/user_details.html', user=user_profile, posts=user_posts)



@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template('users/new_users.html')


@app.route('/users/new', methods=["POST"])
def users_create():
    """Handle form submission for creating a new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user_form(user_id):
    """Show form to edit user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit_users.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_users(user_id):
    """Hand delete users formr"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# ************************************ posts routes ****************************************

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def posts_new_form(user_id):
    """Show post form form"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new_post_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show a page post info"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_detail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    user = post.user  
    return render_template('posts/edit_page_post.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Form handler for updating a post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Form handler for deleting post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")
