from functools import wraps
from flask import session, redirect, url_for, flash
from utils.patient_utils import get_user_role

# Decorators for route protection

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for an admin

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue', 'warning')
            return redirect(url_for('login'))
        
        role = get_user_role(session['user_id'])
        
        if role != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for a doctor

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue', 'warning')
            return redirect(url_for('login'))
        
        role = get_user_role(session['user_id'])
        
        if role !='doctor':
            flash('Doctor access required', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function