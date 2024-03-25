"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///biolgy_new'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
toolbar = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)


@app.route('/')
def Home_Page():
    """Home page"""

    return redirect("/users")

@app.route('/users')
def all_users():
    """Show all users page."""
    users = User.query.all()
    return render_template('users.html',users=users)


@app.route('/<int:id>')
def profiles(id):
    """Show each user."""
    user_profile = User.query.get_or_404(id)
    return render_template('details.html', user = user_profile)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template('new_users.html')


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


@app.route('/users/<int:id>/edit', methods=["GET"])
def edit_user_form(id):
    """Show form to edit user"""
    user = User.query.get_or_404(id)
    return render_template('edit_users.html', user=user)


@app.route('/users/<int:id>/edit', methods=["POST"])
def users_update(id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_users(id):
    """Hand delet users formr"""

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


