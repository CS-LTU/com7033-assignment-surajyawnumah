from datetime import datetime
import re
import sqlite3

# Validation for user role

def get_user_role(user_id):
    conn = sqlite3.connect('stroke_project.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Validation for patient data

def validate_patient(first_name, last_name, gender, date_of_birth, email=None):
    if not all([first_name, last_name, first_name.strip(), last_name.strip()]):
        raise ValueError('First name and last name are required')
    
    if email is not None:
        if not email:
            raise ValueError('Email is required')
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError('Invalid email format')
    
    valid_genders = ['Male', 'Female', 'Other']
    if not gender:
        raise ValueError('Gender is required')
    if gender not in valid_genders:
        raise ValueError('Invalid gender selection')
    
    if not date_of_birth:
        raise ValueError('Date of birth is required')
    
    try:
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Invalid date format')
    
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    if age < 0:
        raise ValueError('Date of birth cannot be in the future')
    if age > 120:
        raise ValueError('Invalid age')
    
    return True