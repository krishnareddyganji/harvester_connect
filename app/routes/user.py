from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from app.models import User

user = Blueprint('user', __name__)

@user.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard for all logged‑in users.
    Displays a welcome and any user‑specific info.
    """
    return render_template('dashboard.html', user=current_user)

@user.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """
    Search for harvester owners by village.
    - GET: show the search form
    - POST: query owners in the given village, display results
    """
    results = []
    if request.method == 'POST':
        village = request.form.get('village', '').strip()
        if not village:
            flash("Please enter a village name to search.", "warning")
        else:
            # Only return users with role='owner'
            results = User.query.filter_by(role='owner', village=village).all()
            if not results:
                flash(f"No harvester owners found in '{village}'.", "info")

    return render_template('search.html', results=results)
