# app/routes/owner.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import db, Harvester

owner_bp = Blueprint('owner', __name__, url_prefix='/owner')

@owner_bp.route('/add-harvester', methods=['GET', 'POST'])
@login_required
def add_harvester():
    if current_user.role != 'owner':
        abort(403)

    if request.method == 'POST':
        harvester_type = request.form['type']
        vehicle_number = request.form['vehicle_number']
        contact = request.form['contact']

        new_harvester = Harvester(
            owner_id=current_user.id,
            type=harvester_type,
            vehicle_number=vehicle_number,
            contact=contact
        )

        db.session.add(new_harvester)
        db.session.commit()
        flash('Harvester details added successfully.')
        return redirect(url_for('owner.add_harvester'))

    return render_template('owner/add_harvester.html')
