from flask import render_template, Flask, request, flash, redirect, url_for, session
from models.user import User
from models.patient import Patient
from init_db import init_database
from utils.decorators import auth_required, admin_required, doctor_required
from utils.patient_utils import validate_patient, get_user_role
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

init_database()

# Route for home page

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

# Route for about page

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

# Route for login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            
            if not email or not password:
                raise ValueError('Email and password are required')
            
            user = User.authenticate_user(email, password)
            
            if user:
                session['user_id'] = user.id
                flash(f'Welcome back, {user.first_name}!', 'success')
                return redirect(url_for('patient_managment'))
            else:
                raise ValueError('Invalid email or password')
                
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'danger')
            return render_template('login.html')
    
    return render_template('login.html')

# Route for registration page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            role = request.form.get('role', '').strip()
            
 
            if not all ([first_name, last_name, email, password, confirm_password]):
                raise ValueError('All fields are required')
            
            if password != confirm_password:
                raise ValueError('Passwords do not match')
            
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, email):
                raise ValueError('Please enter a valid email address') 
        
            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$'
            if not re.match(pattern, password):
                raise ValueError('Password must be 8+ chars and include upper, lower, digit and special char.')

            if User.email_exists(email):
                raise ValueError('Email already exists')
        
            if User.create_user(first_name, last_name, email, role, password):
                flash('Registration successful! Please login', 'success')
                return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

# Route for patient management dashboard

@app.route('/patient-management')
@auth_required
def patient_managment():
    user_role = get_user_role(session['user_id'])
    patients = Patient.get_all_patients()
    return render_template('patient_management.html', patients=patients, user_role=user_role)

# Route to add a new patient

@app.route('/add-patient', methods=['POST'])
@admin_required
def add_patient():
    try:
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        gender = request.form.get('gender', '').strip()
        date_of_birth = request.form.get('date_of_birth', '').strip()
        
        validate_patient(first_name, last_name, gender, date_of_birth, email)
        
        Patient.create_patient(first_name, last_name, email, gender, date_of_birth, session['user_id'])
        flash('Patient added successfully', 'success')
    except Exception as e:
        flash(f'Failed to add patient: {str(e)}', 'danger')
    
    return redirect(url_for('patient_managment'))

# Route to edit a patient

@app.route('/edit-patient/<int:patient_id>')
@doctor_required
def edit_patient(patient_id):
    patient = Patient.get_patient_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'danger')
        return redirect(url_for('patient_managment'))
    return render_template('edit_patient.html', patient=patient)

# Route to update a patient

@app.route('/update-patient/<int:patient_id>', methods=['POST'])
@doctor_required
def update_patient(patient_id):
    try:
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        gender = request.form.get('gender', '').strip()
        date_of_birth = request.form.get('date_of_birth', '').strip()
        
        validate_patient(first_name, last_name, gender, date_of_birth)
        
        Patient.update_patient(patient_id, first_name, last_name, gender, date_of_birth)
        flash('Patient updated successfully', 'success')
    except Exception as e:
        flash(f'Failed to update patient: {str(e)}', 'danger')
    
    return redirect(url_for('edit_patient', patient_id=patient_id))

# Route to delete a patient

@app.route('/delete-patient/<int:patient_id>', methods=['POST'])
@admin_required
def delete_patient(patient_id):
    try:
        Patient.delete_patient(patient_id)
        flash('Patient deleted successfully', 'success')
    except Exception as e:
        flash(f'Failed to delete patient: {str(e)}', 'danger')
    return redirect(url_for('patient_managment'))

# Route to logout

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))

# Main execution
if __name__ == '__main__':
    app.run(debug=True, port=8080)