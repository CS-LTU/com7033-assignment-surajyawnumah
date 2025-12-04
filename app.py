from flask import render_template, Flask, request, flash, redirect, url_for
from models.user import User
from init_db import init_database
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

init_database()


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

@app.route('/login')
def login():
    """Render the login page."""
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
def patient_managment():
    """Render the patient management page."""
    return render_template('patient_management.html')

# Main execution
if __name__ == '__main__':
    app.run(debug=True, port=8080)