from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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

    return render_template("users/homepage.html")   

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
    # this is showing the users new post page
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new_post_form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    selected_tags = request.form.getlist('tags')
    new_post = Post(title=title, content=content, user=user)
    
    for tag_id in selected_tags:
        tag = Tag.query.get_or_404(tag_id)
        new_post.tags.append(tag)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show a page post info"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = Tag.query.all()
    return render_template('posts/edit_page_post.html', post=post, user=user, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Form handler for updating a post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    post.tags.clear()

    selected_tags = request.form.getlist('tags')
    for tag_id in selected_tags:
        tag = Tag.query.get_or_404(tag_id)
        post.tags.append(tag)

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
 
# ************************************ tag routes ****************************************


@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/tags_all.html', tags=tags)


@app.route('/new/tags')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new_tags.html')


@app.route("/new/tags", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""
    tag_name = request.form['tag_name']
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")
    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_page(tag_id):
    """Show a page with a certain tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag_page.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/tag_edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    # This line retrieves a list of post IDs from the checkboxes, assigns them as ints
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tags(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
