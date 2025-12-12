from init_db import init_database
import csv
from pathlib import Path
from datetime import datetime

from models.user import User
from models.patient import Patient
from models.mongo.assessment_model import create_assessment

# Base directory 
BASE_DIR = Path(__file__).resolve().parent

# CSV with initial data
CSV_PATH = BASE_DIR / "seeded_dataset.csv"

# Marker file so the seed only runs once
SEED_MARKER = BASE_DIR / ".seed_has_run"


def seed_admin_and_doctor_users():
    """
    Create default admin and doctor users in SQLite if they don't already exist.
    WARNING: These passwords are for development/demo only. DO NOT use in production.
    """
    admin_email = "admin@example.com"
    doctor_email = "doctor@example.com"

    if not User.email_exists(admin_email):
        User.create_user(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            role="admin",
            password="Admin123!"  
        )
        print("[seed_data] Created default admin user")

    if not User.email_exists(doctor_email):
        User.create_user(
            first_name="Doctor",
            last_name="User",
            email=doctor_email,
            role="doctor",
            password="Doctor123!"  
        )
        print("[seed_data] Created default doctor user")


def _parse_int(value, default=0):
    """
    Safely parse an int from CSV data.
    Accepts '1', '0', '1.0', etc. Returns default on error/blank.
    """
    if value is None:
        return default
    s = str(value).strip()
    if s == "":
        return default
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return default


def _parse_float(value, default=0.0):
    """
    Safely parse a float from CSV data.
    """
    if value is None:
        return default
    s = str(value).strip()
    if s == "":
        return default
    try:
        return float(s)
    except (ValueError, TypeError):
        return default


def seed_patients_and_assessments_from_csv():
    """
    Seed patients (SQLite) and stroke assessments (MongoDB) from CSV.

    Adjust the column names in row.get(...) below to match your CSV header.
    Common stroke dataset headers look like:
      first_name, last_name, email, gender, age,
      hypertension, ever_married, work_type, Residence_type (or residence_type),
      avg_glucose_level, bmi, smoking_status, stroke
    """
    if not CSV_PATH.exists():
        print(f"[seed_data] CSV not found at {CSV_PATH}, skipping patient seeding.")
        return

    print(f"[seed_data] Seeding patients & assessments from {CSV_PATH}")

    # Use admin user (created above) - should have ID 1 in fresh DB
    # Verify admin exists before proceeding
    if not User.email_exists("admin@example.com"):
        print("[seed_data] Admin user not found, cannot seed patients.")
        return
    created_by_user_id = 1  

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Validate required CSV columns
        required_cols = ['first_name', 'last_name', 'email', 'gender', 'age']
        if not all(col in reader.fieldnames for col in required_cols):
            print(f"[seed_data] ERROR: CSV missing required columns. Found: {reader.fieldnames}")
            print(f"[seed_data] Required: {required_cols}")
            return

        for row in reader:
            # PATIENT FIELDS (SQLite)
            first_name = (row.get("first_name") or "").strip()
            last_name = (row.get("last_name") or "").strip()
            email = (row.get("email") or "").strip()
            gender = (row.get("gender") or "").strip()

            # Convert age to an approximate DOB.
            age_str = (row.get("age") or "").strip()
            date_of_birth = "1970-01-01"  #

            if age_str:
                try:
                    age = int(float(age_str))
                    # Rough DOB: current_year - age 
                    approx_year = datetime.now().year - age
                    date_of_birth = f"{approx_year}-01-01"
                except ValueError:
                    # If age can't be parsed, we just keep the default DOB
                    pass

            # Create patient and get its auto-incremented ID from SQLite
            try:
                patient_id = Patient.create_patient(
                    first_name,
                    last_name,
                    email,
                    gender,
                    date_of_birth,
                    created_by_user_id
                )
            except Exception as e:
                print(f"[seed_data] Failed to create patient {email}: {e}")
                continue

            # ASSESSMENT FIELDS (MongoDB) 
            hypertension = _parse_int(row.get("hypertension"), default=0)
            heart_disease = _parse_int(row.get("heart_disease"), default=0)
            ever_married = (row.get("ever_married") or "").strip()
            work_type = (row.get("work_type") or "").strip()

            # Some datasets use "Residence_type", others "residence_type"
            residence_type = (
                (row.get("Residence_type")
                 or row.get("residence_type")
                 or "").strip()
            )

            avg_glucose_level = _parse_float(row.get("avg_glucose_level"), default=0.0)
            bmi = _parse_float(row.get("bmi"), default=0.0)
            smoking_status = (row.get("smoking_status") or "").strip()
            stroke = _parse_int(row.get("stroke"), default=0)

            
            if patient_id:  
                try:
                    create_assessment(
                        patient_id,
                        hypertension,
                        heart_disease,
                        ever_married,
                        work_type,
                        residence_type,
                        avg_glucose_level,
                        bmi,
                        smoking_status,
                        stroke,
                    )
                except Exception as e:
                    print(f"[seed_data] Failed to create assessment for patient {patient_id}: {e}")

    print("[seed_data] Finished seeding patients and assessments.")


def run_seed_if_needed():
    """
    Public function to run seeding exactly once.
    - Call this from app.py after init_database()
    - You can also call this from a standalone script like run_seed_once.py
    """
    if SEED_MARKER.exists():
        print("[seed_data] Seed marker found, skipping seeding.")
        return

    print("[seed_data] No seed marker found, running full seed...")

    # 1) Make sure core users exist in SQLite
    seed_admin_and_doctor_users()

    # 2) Seed patients in SQLite + assessments in MongoDB from CSV
    seed_patients_and_assessments_from_csv()

    # 3) Create marker so this doesn't run again
    SEED_MARKER.write_text("done\n")
    print(f"[seed_data] Seeding complete. Marker created at {SEED_MARKER}")


if __name__ == '__main__':
    init_database()
    run_seed_if_needed()