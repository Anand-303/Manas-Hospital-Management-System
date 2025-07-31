from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import mongo
from bson.objectid import ObjectId
from datetime import datetime

bp = Blueprint('patient', __name__, url_prefix='/patient')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))
    return render_template('patient/dashboard.html')

@bp.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))
    doctors = list(mongo.db.users.find({'role': 'doctor'}))
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        reason = request.form['reason']
        appointment = {
            'patient_id': ObjectId(current_user.id),
            'doctor_id': ObjectId(doctor_id),
            'date': datetime.strptime(date, '%Y-%m-%dT%H:%M'),
            'reason': reason,
            'status': 'pending'
        }
        mongo.db.appointments.insert_one(appointment)
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient.appointments'))
    # List appointments for this patient
    appointments = list(mongo.db.appointments.find({'patient_id': ObjectId(current_user.id)}))
    # Attach doctor info to each appointment
    for appt in appointments:
        appt['doctor'] = mongo.db.users.find_one({'_id': appt['doctor_id']})
    return render_template('patient/appointments.html', doctors=doctors, appointments=appointments)

@bp.route('/doctors')
@login_required
def view_doctors():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))
    doctors = list(mongo.db.users.find({'role': 'doctor'}))
    return render_template('patient/doctors.html', doctors=doctors)

@bp.route('/beds')
@login_required
def check_beds():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))
    beds = list(mongo.db.beds.find())
    return render_template('patient/beds.html', beds=beds)

@bp.route('/facilities')
@login_required
def view_facilities():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))
    facilities = list(mongo.db.facilities.find())
    return render_template('patient/facilities.html', facilities=facilities)

@bp.route('/medications', methods=['GET', 'POST'])
@login_required
def buy_medication():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))
    medications = list(mongo.db.medications.find())
    if request.method == 'POST':
        med_id = request.form['med_id']
        quantity = int(request.form['quantity'])
        med = mongo.db.medications.find_one({'_id': ObjectId(med_id)})
        if med and med['stock'] >= quantity:
            mongo.db.medications.update_one({'_id': ObjectId(med_id)}, {'$inc': {'stock': -quantity}})
            purchase = {
                'patient_id': ObjectId(current_user.id),
                'med_id': ObjectId(med_id),
                'quantity': quantity,
                'date': datetime.now()
            }
            mongo.db.purchases.insert_one(purchase)
            flash('Medication purchased successfully!', 'success')
        else:
            flash('Not enough stock for this medication.', 'danger')
        return redirect(url_for('patient.buy_medication'))
    return render_template('patient/medications.html', medications=medications) 