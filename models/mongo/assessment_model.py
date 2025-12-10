from config import Config
from bson.objectid import ObjectId
from models.mongo.connection import mongo_conn

def get_assessment_collection():
    client, mdb = mongo_conn()
    if client is None:
        return None, None
    assessment_coll = mdb[Config.MONGO_ASSESSMENT_COL]
    return client, assessment_coll

def get_assessments_by_patient_id(patient_id):
    client, coll = get_assessment_collection()
    if coll is None:
        return []
    
    assessments = list(coll.find({"patient_id": int(patient_id)}))
    client.close()
    return assessments

def create_assessment(patient_id, hypertension, ever_married, work_type, residence_type, 
                     avg_glucose_level, bmi, smoking_status, stroke):
    client, coll = get_assessment_collection()
    if coll is None:
        return None
    
    new_assessment = {
        "patient_id": int(patient_id),
        "hypertension": int(hypertension),
        "ever_married": ever_married,
        "work_type": work_type,
        "residence_type": residence_type,
        "avg_glucose_level": float(avg_glucose_level),
        "bmi": float(bmi),
        "smoking_status": smoking_status,
        "stroke": int(stroke)
    }
    result = coll.insert_one(new_assessment)
    client.close()
    return str(result.inserted_id)