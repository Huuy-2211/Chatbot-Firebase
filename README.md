# Chatbot-Firebase

## 1. Thông tin sinh viên
Họ và tên: Lê Đình Huy  
Mã số sinh viên: 24120324  
Lớp: TDTT-CTT3  

## 2. Hướng dẫn cài đặt environment
Yêu cầu Python 3.10 trở lên.

Tạo môi trường ảo:
python -m venv venv  

Kích hoạt môi trường ảo:
.\venv\Scripts\activate  

Cài đặt thư viện:
pip install -r requirements.txt  

## 3. Cấu hình biến môi trường (.env)
Tạo file `.env` tại thư mục gốc và thêm:

GEMINI_API_KEY 

FIREBASE_WEB_API_KEY

FIREBASE_KEY_PATH=serviceAccountKey.json  

## 4. Thiết lập Firebase
Truy cập Firebase Console → Project Settings → Service Accounts → Generate new private key → tải file JSON → đổi tên thành `serviceAccountKey.json` → đặt vào thư mục `backend/`  

## 5. Hướng dẫn chạy backend
cd backend  
python main.py  

## 6. Hướng dẫn chạy frontend
cd frontend  
streamlit run app.py  

## 7. Tài khoản đăng nhập hệ thống
email: huy123@gmail.com
mk: 101106
## 8. Đường dẫn đến video demo
https://github.com/user-attachments/assets/07f900ea-39c7-4877-bd01-e0769aa25348










