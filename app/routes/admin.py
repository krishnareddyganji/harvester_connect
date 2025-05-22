# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import db, User, Harvester

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    users = User.query.all()
    harvesters = Harvester.query.all()
    return render_template('admin/dashboard.html', users=users, harvesters=harvesters)

@admin.route('/delete_user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted')
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete_harvester/<int:id>', methods=['POST'])
@login_required
def delete_harvester(id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    harvester = Harvester.query.get_or_404(id)
    db.session.delete(harvester)
    db.session.commit()
    flash('Harvester deleted')
    return redirect(url_for('admin.dashboard'))

@admin.route('/page')
@login_required
def admin_page():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')
