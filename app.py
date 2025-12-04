
"""
StrokePredictionApp
Secure Healthcare Application
"""

from flask import Config, Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response
from flask_sqlalchemy import SQLAlchemy



# Initialize application
app = Flask(__name__)

#===========================================================
# Configuration
# Application Routes
#============================================================

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

@app.route('/login')
def login():
    """Render the login page."""
    return render_template('login.html')

# Route for registration page

@app.route('/register')
def register():
    """Render the registration page."""
    return render_template('register.html')

# Route for patient management dashboard

@app.route('/patient-management')
def patient_managment():
    """Render the patient management page."""
    return render_template('patient_management.html')

# Main execution
if __name__ == '__main__':
    app.run(debug=True)