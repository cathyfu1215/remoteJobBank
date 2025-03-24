import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables from .env file
def load_env_vars():
    dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(dotenv_path)

# Firebase initialization
def get_firebase_credentials():
    load_env_vars()
    return {
        "type": os.getenv("FIREBASE_TYPE"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"), 
        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
    }

# Initialize Firebase and return firestore client
def get_firestore_client():
    if not firebase_admin._apps:
        firebase_cred = get_firebase_credentials()
        cred = credentials.Certificate(firebase_cred)
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Database operations
def exists_in_collection(collection_name, doc_id):
    """Check if a document already exists in the specified Firestore collection"""
    try:
        db = get_firestore_client()
        doc_ref = db.collection(collection_name).document(doc_id)
        return doc_ref.get().exists
    except Exception as e:
        print(f"Error checking document existence: {e}")
        # In case of error, return False to allow processing attempt
        return False

def save_to_collection(collection_name, data, doc_id=None, dry_run=False):
    """Save data to Firestore collection, avoiding duplicates"""
    try:
        if not doc_id and 'job_id' in data:
            doc_id = data['job_id']
        elif not doc_id:
            raise ValueError("Document ID not provided")
            
        if dry_run:
            print(f"🚨 Dry Run: Would save document {doc_id}")
            return True
        
        db = get_firestore_client()
        doc_ref = db.collection(collection_name).document(doc_id)
        
        # Check if document exists
        if not doc_ref.get().exists:
            doc_ref.set(data)
            print(f"✅ Saved document: {doc_id}")
            return True
        else:
            print(f"⏩ Document already exists: {doc_id}")
            return False
    except Exception as e:
        print(f"❌ Firestore error: {e}")
        return False 