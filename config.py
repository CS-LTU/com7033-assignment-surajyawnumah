from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    BASE_DIR = os.getcwd()
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_me_dev_key")
    DB_PATH = os.path.join(BASE_DIR, "stroke_project.db")

    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DB = os.environ.get("MONGO_DB", "stroke_project")
    MONGO_ALLERGY_COL = os.environ.get("MONGO_ALLERGY_COL", "allergies")
    MONGO_ASSESSMENT_COL = os.environ.get("MONGO_ASSESSMENT_COL", "assessments")