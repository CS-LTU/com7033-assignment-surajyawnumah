import unittest
from app import app
import sqlite3
import os

TEST_DB = 'test_stroke_project.db'  

def create_test_database():
    """Create test database with users table"""
    
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    cursor.execute(''' 
        INSERT INTO users (first_name, last_name, email, password_hash, role)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Rhaj', 'Ash', 'rhaj@example.com', 'hashed_password_123', 'doctor'))
    
    conn.commit() 
    conn.close()


def user_in_db(email):
    """Check if user exists in database"""
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return user is not None


class StrokePredictionTest(unittest.TestCase):
    """Test cases for Stroke Prediction System"""
    
    def setUp(self):
        """Set up test client and database"""
        create_test_database()  
        
        self.email = "rhaj@example.com"
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
    
    def test_login_page(self):
        """Test that login page loads"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_register_page(self):
        """Test that register page loads"""
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
    
    def test_user_creation(self):
        """Test user exists in database"""
        self.assertTrue(
            user_in_db(self.email),
            f"User with email {self.email} should exist in the database."
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)