from config import Config
from bson.objectid import ObjectId
from models.mongo.connection import mongo_conn

def get_allergy_collection():
    client, mdb = mongo_conn()
    if client is None:
        return None, None
    allergy_coll = mdb[Config.MONGO_ALLERGY_COL]
    return client, allergy_coll

def get_allergies_by_patient_id(patient_id):
    client, coll = get_allergy_collection()
    if coll is None:
        return []
    
    allergies = list(coll.find({"patient_id": int(patient_id)}))
    client.close()
    return allergies

def create_allergy(patient_id, allergen, severity, date_added):
    client, coll = get_allergy_collection()
    if coll is None:
        return None
    
    new_allergy = {
        "patient_id": int(patient_id),
        "allergen": allergen,
        "severity": severity,
        "date_added": date_added
    }
    result = coll.insert_one(new_allergy)
    client.close()
    return str(result.inserted_id)

def get_allergy_by_id(allergy_id):
    client, coll = get_allergy_collection()
    if coll is None:
        return None
    
    allergy = coll.find_one({"_id": ObjectId(allergy_id)})
    client.close()
    return allergy

def update_allergy(allergy_id, patient_id, allergen, severity, date_added):
    client, coll = get_allergy_collection()
    if coll is None:
        return False
    
    updated_allergy = {
        "allergen": allergen,
        "severity": severity,
        "date_added": date_added
    }
    result = coll.update_one(
        {"_id": ObjectId(allergy_id), "patient_id": int(patient_id)},
        {"$set": updated_allergy}
    )
    client.close()
    return result.modified_count > 0

def delete_allergy(allergy_id):
    client, coll = get_allergy_collection()
    if coll is None:
        return False
    
    result = coll.delete_one({"_id": ObjectId(allergy_id)})
    client.close()
    return result.deleted_count > 0