from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import mongo
from bson.objectid import ObjectId

bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'doctor':
        return redirect(url_for('auth.login'))
    return render_template('doctor/dashboard.html')

@bp.route('/patients')
@login_required
def patients():
    if current_user.role != 'doctor':
        return redirect(url_for('auth.login'))
    assigned_patients = list(mongo.db.users.find({'role': 'patient', 'assigned_doctor': ObjectId(current_user.id)}))
    return render_template('doctor/patients.html', patients=assigned_patients)

@bp.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    if current_user.role != 'doctor':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        appt_id = request.form['appt_id']
        status = request.form['status']
        mongo.db.appointments.update_one({'_id': ObjectId(appt_id)}, {'$set': {'status': status}})
        flash('Appointment status updated!', 'success')
        return redirect(url_for('doctor.appointments'))
    appointments = list(mongo.db.appointments.find({'doctor_id': ObjectId(current_user.id)}))
    for appt in appointments:
        appt['patient'] = mongo.db.users.find_one({'_id': appt['patient_id']})
    return render_template('doctor/appointments.html', appointments=appointments)

@bp.route('/update_status', methods=['GET', 'POST'])
@login_required
def update_status():
    if current_user.role != 'doctor':
        return redirect(url_for('auth.login'))
    assigned_patients = list(mongo.db.users.find({'role': 'patient', 'assigned_doctor': ObjectId(current_user.id)}))
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        treatment_notes = request.form['treatment_notes']
        status = request.form['status']
        mongo.db.users.update_one({'_id': ObjectId(patient_id)}, {'$set': {'treatment_notes': treatment_notes, 'treatment_status': status}})
        flash('Patient status updated!', 'success')
        return redirect(url_for('doctor.update_status'))
    # Attach treatment info to each patient
    for patient in assigned_patients:
        patient['treatment_notes'] = patient.get('treatment_notes', '')
        patient['treatment_status'] = patient.get('treatment_status', '')
    return render_template('doctor/update_status.html', patients=assigned_patients)

# Additional routes for doctor features will be added here 