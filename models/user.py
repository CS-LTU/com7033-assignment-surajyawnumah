import sqlite3
from werkzeug.security import generate_password_hash

class User:
    def __init__(self, first_name, last_name, email, role, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.role = role
        self.password_hash = password_hash

    @staticmethod
    def email_exists(email):
        
        conn = sqlite3.connect('stroke_project.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    @staticmethod
    def create_user(first_name, last_name, email, role, password):
        
        password_hash = generate_password_hash(password)
        
        conn = sqlite3.connect('stroke_project.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, role, password_hash)
            VALUES (?, ?, ?, ?, ?)
            
        ''', (first_name, last_name, email, role, password_hash))
        conn.commit()
        conn.close()
        return True