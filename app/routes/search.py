from flask import Blueprint, request, render_template
from app.models import User
from app import db
from sqlalchemy.orm import joinedload

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    village = ''
    query = User.query.options(joinedload(User.harvesters)).filter(User.role == 'owner')

    if request.method == 'POST':
        village = request.form.get('village', '').strip()
        if village:
            query = query.filter(User.village.ilike(f'%{village}%'))

    results = query.all()  # Always run the query and send results to the template
    return render_template('search.html', results=results, village=village)
