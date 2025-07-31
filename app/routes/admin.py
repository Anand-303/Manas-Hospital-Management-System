from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import mongo
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')

@bp.route('/doctors', methods=['GET', 'POST'])
def manage_doctors():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        specialization = request.form['specialization']
        if mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Username or email already exists', 'danger')
        else:
            hashed_pw = generate_password_hash(password)
            user_doc = {
                'username': username,
                'email': email,
                'password': hashed_pw,
                'role': 'doctor',
                'specialization': specialization
            }
            mongo.db.users.insert_one(user_doc)
            flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))
    doctors = list(mongo.db.users.find({'role': 'doctor'}))
    return render_template('admin/doctors.html', doctors=doctors)

@bp.route('/doctors/edit/<doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    doctor = mongo.db.users.find_one({'_id': ObjectId(doctor_id), 'role': 'doctor'})
    if not doctor:
        flash('Doctor not found.', 'danger')
        return redirect(url_for('admin.manage_doctors'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        specialization = request.form['specialization']
        update_doc = {
            'username': username,
            'email': email,
            'specialization': specialization
        }
        if request.form['password']:
            update_doc['password'] = generate_password_hash(request.form['password'])
        mongo.db.users.update_one({'_id': ObjectId(doctor_id)}, {'$set': update_doc})
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))
    return render_template('admin/edit_doctor.html', doctor=doctor)

@bp.route('/doctors/delete/<doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    mongo.db.users.delete_one({'_id': ObjectId(doctor_id), 'role': 'doctor'})
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('admin.manage_doctors'))

@bp.route('/patients', methods=['GET', 'POST'])
def manage_patients():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Username or email already exists', 'danger')
        else:
            hashed_pw = generate_password_hash(password)
            user_doc = {
                'username': username,
                'email': email,
                'password': hashed_pw,
                'role': 'patient'
            }
            mongo.db.users.insert_one(user_doc)
            flash('Patient added successfully!', 'success')
        return redirect(url_for('admin.manage_patients'))
    patients = list(mongo.db.users.find({'role': 'patient'}))
    return render_template('admin/patients.html', patients=patients)

@bp.route('/patients/edit/<patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    patient = mongo.db.users.find_one({'_id': ObjectId(patient_id), 'role': 'patient'})
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('admin.manage_patients'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        update_doc = {
            'username': username,
            'email': email
        }
        if request.form['password']:
            update_doc['password'] = generate_password_hash(request.form['password'])
        mongo.db.users.update_one({'_id': ObjectId(patient_id)}, {'$set': update_doc})
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('admin.manage_patients'))
    return render_template('admin/edit_patient.html', patient=patient)

@bp.route('/patients/delete/<patient_id>', methods=['POST'])
def delete_patient(patient_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    mongo.db.users.delete_one({'_id': ObjectId(patient_id), 'role': 'patient'})
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('admin.manage_patients'))

@bp.route('/beds', methods=['GET', 'POST'])
def manage_beds():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        bed_type = request.form['bed_type']
        is_available = request.form.get('is_available') == 'on'
        bed_doc = {
            'bed_type': bed_type,
            'is_available': is_available
        }
        mongo.db.beds.insert_one(bed_doc)
        flash('Bed added successfully!', 'success')
        return redirect(url_for('admin.manage_beds'))
    beds = list(mongo.db.beds.find())
    return render_template('admin/beds.html', beds=beds)

@bp.route('/beds/edit/<bed_id>', methods=['GET', 'POST'])
def edit_bed(bed_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    bed = mongo.db.beds.find_one({'_id': ObjectId(bed_id)})
    if not bed:
        flash('Bed not found.', 'danger')
        return redirect(url_for('admin.manage_beds'))
    if request.method == 'POST':
        bed_type = request.form['bed_type']
        is_available = request.form.get('is_available') == 'on'
        update_doc = {
            'bed_type': bed_type,
            'is_available': is_available
        }
        mongo.db.beds.update_one({'_id': ObjectId(bed_id)}, {'$set': update_doc})
        flash('Bed updated successfully!', 'success')
        return redirect(url_for('admin.manage_beds'))
    return render_template('admin/edit_bed.html', bed=bed)

@bp.route('/beds/delete/<bed_id>', methods=['POST'])
def delete_bed(bed_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    mongo.db.beds.delete_one({'_id': ObjectId(bed_id)})
    flash('Bed deleted successfully!', 'success')
    return redirect(url_for('admin.manage_beds'))

@bp.route('/facilities', methods=['GET', 'POST'])
def manage_facilities():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        facility_doc = {
            'name': name,
            'description': description
        }
        mongo.db.facilities.insert_one(facility_doc)
        flash('Facility added successfully!', 'success')
        return redirect(url_for('admin.manage_facilities'))
    facilities = list(mongo.db.facilities.find())
    return render_template('admin/facilities.html', facilities=facilities)

@bp.route('/facilities/edit/<facility_id>', methods=['GET', 'POST'])
def edit_facility(facility_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    facility = mongo.db.facilities.find_one({'_id': ObjectId(facility_id)})
    if not facility:
        flash('Facility not found.', 'danger')
        return redirect(url_for('admin.manage_facilities'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        update_doc = {
            'name': name,
            'description': description
        }
        mongo.db.facilities.update_one({'_id': ObjectId(facility_id)}, {'$set': update_doc})
        flash('Facility updated successfully!', 'success')
        return redirect(url_for('admin.manage_facilities'))
    return render_template('admin/edit_facility.html', facility=facility)

@bp.route('/facilities/delete/<facility_id>', methods=['POST'])
def delete_facility(facility_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    mongo.db.facilities.delete_one({'_id': ObjectId(facility_id)})
    flash('Facility deleted successfully!', 'success')
    return redirect(url_for('admin.manage_facilities'))

@bp.route('/medications', methods=['GET', 'POST'])
def manage_medications():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        med_doc = {
            'name': name,
            'price': price,
            'stock': stock
        }
        mongo.db.medications.insert_one(med_doc)
        flash('Medication added successfully!', 'success')
        return redirect(url_for('admin.manage_medications'))
    medications = list(mongo.db.medications.find())
    return render_template('admin/medications.html', medications=medications)

@bp.route('/medications/edit/<med_id>', methods=['GET', 'POST'])
def edit_medication(med_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    med = mongo.db.medications.find_one({'_id': ObjectId(med_id)})
    if not med:
        flash('Medication not found.', 'danger')
        return redirect(url_for('admin.manage_medications'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        update_doc = {
            'name': name,
            'price': price,
            'stock': stock
        }
        mongo.db.medications.update_one({'_id': ObjectId(med_id)}, {'$set': update_doc})
        flash('Medication updated successfully!', 'success')
        return redirect(url_for('admin.manage_medications'))
    return render_template('admin/edit_medication.html', med=med)

@bp.route('/medications/delete/<med_id>', methods=['POST'])
def delete_medication(med_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    mongo.db.medications.delete_one({'_id': ObjectId(med_id)})
    flash('Medication deleted successfully!', 'success')
    return redirect(url_for('admin.manage_medications'))

@bp.route('/assign', methods=['GET', 'POST'])
def assign():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    patients = list(mongo.db.users.find({'role': 'patient'}))
    doctors = list(mongo.db.users.find({'role': 'doctor'}))
    beds = list(mongo.db.beds.find({'is_available': True}))
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        bed_id = request.form['bed_id']
        # Assign doctor and bed to patient
        mongo.db.users.update_one({'_id': ObjectId(patient_id)}, {'$set': {'assigned_doctor': ObjectId(doctor_id), 'assigned_bed': ObjectId(bed_id)}})
        # Mark bed as unavailable
        mongo.db.beds.update_one({'_id': ObjectId(bed_id)}, {'$set': {'is_available': False}})
        flash('Doctor and bed assigned to patient successfully!', 'success')
        return redirect(url_for('admin.assign'))
    # Show current assignments
    assignments = []
    for patient in patients:
        doctor = None
        bed = None
        if 'assigned_doctor' in patient:
            doctor = mongo.db.users.find_one({'_id': patient['assigned_doctor']})
        if 'assigned_bed' in patient:
            bed = mongo.db.beds.find_one({'_id': patient['assigned_bed']})
        assignments.append({'patient': patient, 'doctor': doctor, 'bed': bed})
    return render_template('admin/assign.html', patients=patients, doctors=doctors, beds=beds, assignments=assignments) 