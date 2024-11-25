import firebase_admin
from firebase_admin import credentials, firestore

from dotenv import load_dotenv
load_dotenv()

cert = credentials.Certificate("firebase.json")
app = firebase_admin.initialize_app(credential=cert)
db = firestore.client()

def add_user(user: dict):
    try:
        True
        doc_ref = db.collection("users").document()
        doc_id = doc_ref.id
        doc_ref.set(user)
        
        user_ref = db.collection("users").document(doc_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            user_data_full = {
                "id": user_ref.id,
                **user_data
            }
            
            print(user_data_full)
        else:
            print("User not found.")
            raise KeyError(f"User  wih id {doc_id} doesn't exist")
        
        return user_data_full
    except Exception as e:
        print("Error adding user:", e)
        raise e
