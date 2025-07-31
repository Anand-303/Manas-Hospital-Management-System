from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from .. import mongo, login_manager

bp = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']
        self.email = user_doc['email']
        self.password = user_doc['password']
        self.role = user_doc['role']

@login_manager.user_loader
def load_user(user_id):
    user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_doc:
        return User(user_doc)
    return None

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_doc = mongo.db.users.find_one({'username': username})
        if user_doc and check_password_hash(user_doc['password'], password):
            user = User(user_doc)
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for(f'{user.role}.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        if mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Username or email already exists', 'danger')
        else:
            hashed_pw = generate_password_hash(password)
            user_doc = {
                'username': username,
                'email': email,
                'password': hashed_pw,
                'role': role
            }
            mongo.db.users.insert_one(user_doc)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html') 