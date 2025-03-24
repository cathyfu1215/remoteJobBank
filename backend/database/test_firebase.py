import os
from firebase_client import get_firestore_client, exists_in_collection, save_to_collection

def test_firebase_connection():
    """Test basic Firebase connectivity"""
    try:
        # Get the Firestore client
        db = get_firestore_client()
        print("✅ Firebase connection successful")
        
        # Test retrieving a collection (won't fail even if empty)
        jobs_ref = db.collection('jobs').limit(1).get()
        print(f"✅ Can query collections: found {len(list(jobs_ref))} documents")
        
        return True
    except Exception as e:
        print(f"❌ Firebase connection failed: {e}")
        return False

def test_document_operations():
    """Test document operations with a temporary test document"""
    test_id = "test_document_" + os.urandom(4).hex()
    test_data = {
        "test_field": "test_value",
        "timestamp": "2023-01-01"
    }
    
    try:
        # Test document creation
        result = save_to_collection('test_collection', test_data, doc_id=test_id)
        if not result:
            print("❌ Failed to save test document")
            return False
        print("✅ Document saved successfully")
        
        # Test document existence check
        exists = exists_in_collection('test_collection', test_id)
        if not exists:
            print("❌ Document existence check failed")
            return False
        print("✅ Document existence check successful")
        
        # Clean up test document
        db = get_firestore_client()
        db.collection('test_collection').document(test_id).delete()
        print("✅ Test document cleaned up")
        
        return True
    except Exception as e:
        print(f"❌ Document operations failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Firebase client module...")
    connection_ok = test_firebase_connection()
    if connection_ok:
        document_ok = test_document_operations()
    else:
        document_ok = False
    
    if connection_ok and document_ok:
        print("\n✅ All Firebase client tests passed!")
    else:
        print("\n❌ Some Firebase client tests failed") 