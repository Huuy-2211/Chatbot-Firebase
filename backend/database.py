from google.cloud.firestore_v1.base_query import FieldFilter
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone

load_dotenv()

try:
    key_path = os.getenv("FIREBASE_KEY_PATH", "serviceAccountKey.json")
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    print("Kết nối Firestore thành công!")
except Exception as e:
    print(f"Lỗi Firebase: {e}")
    db = None
def save_chat_message(user_id: str, role: str, content: str):
    """Lưu tin nhắn (của user hoặc bot) vào database"""
    if not db: return False
    try:
        db.collection("chat_history").add({
            "user_id": user_id,
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc)
        })
        return True
    except Exception as e:
        print(f"Lỗi lưu message: {e}")
        return False

def get_chat_history(user_id: str):
    """Lấy lại lịch sử chat của người dùng """
    if not db: return []
    try:
        docs = db.collection("chat_history")\
                 .where(filter=FieldFilter("user_id", "==", user_id))\
                 .order_by("timestamp", direction=firestore.Query.ASCENDING)\
                 .stream()
        return [{"role": d.to_dict()['role'], "content": d.to_dict()['content']} for d in docs]
    except Exception as e:
        print(f"Lỗi lấy lịch sử: {e}")
        return []