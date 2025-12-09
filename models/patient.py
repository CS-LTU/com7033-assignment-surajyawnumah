import sqlite3

class Patient:
    def __init__(self, id, first_name, last_name, email, gender, date_of_birth, created_by):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.created_by = created_by
    
    # Create a Patient
    
    @staticmethod
    def create_patient(first_name, last_name, email, gender, date_of_birth, created_by):
        conn = sqlite3.connect('stroke_project.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (first_name, last_name, email, gender, date_of_birth, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, gender, date_of_birth, created_by))
        conn.commit()
        conn.close()
        return True
    
    # Retrieve all Patients

    @staticmethod
    def get_all_patients():
        conn = sqlite3.connect('stroke_project.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name, email, gender, date_of_birth, created_by FROM patients')
        rows = cursor.fetchall()
        conn.close()
        patients = []
        for row in rows:
            patients.append(Patient(*row))
        return patients
    
    # Retrieve Patient by ID

    @staticmethod
    def get_patient_by_id(patient_id):
        conn = sqlite3.connect('stroke_project.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, first_name, last_name, email, gender, date_of_birth, created_by FROM patients WHERE id = ?', (patient_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return Patient(*result)
        return None
    
    # Update Patient Information

    @staticmethod
    def update_patient(patient_id, first_name, last_name, gender, date_of_birth):
        conn = sqlite3.connect('stroke_project.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE patients 
            SET first_name = ?, last_name = ?, gender = ?, date_of_birth = ?
            WHERE id = ?
        ''', (first_name, last_name, gender, date_of_birth, patient_id))
        conn.commit()
        conn.close()
        return True
    
    # Delete Patient 

    @staticmethod
    def delete_patient(patient_id):
        conn = sqlite3.connect('stroke_project.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        conn.commit()
        conn.close()
        return True