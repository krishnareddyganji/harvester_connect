# app/routes/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app.models import db, User

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        village = request.form.get('village')
        role = request.form.get('role')
        email = request.form.get('email')
        password = request.form.get('password')

        if not (name and village and role and email and password):
            flash("All fields are required.")
            return redirect(url_for('auth.signup'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already registered.")
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, village=village, role=role, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful! Please log in.")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print(f"Database error: {e}")
            flash("Something went wrong during signup.")
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!')
                return redirect(url_for('user.dashboard'))

            flash('Invalid email or password!')
            return redirect(url_for('auth.login'))

        except Exception as e:
            print(f"Login error: {e}")
            flash('An error occurred during login.')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('auth.login'))


@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, role='admin').first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid admin credentials')
    return render_template('admin_login.html')
