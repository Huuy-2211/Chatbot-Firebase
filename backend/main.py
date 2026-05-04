import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
from database import save_chat_message, get_chat_history

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemma-3-27b-it')
else:
    print(" Thiếu GEMINI_API_KEY trong .env")

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/auth/login")
async def login_endpoint(req: LoginRequest):
    if not FIREBASE_WEB_API_KEY:
        raise HTTPException(status_code=500, detail="Server thiếu Web API Key")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    
    payload = {
        "email": req.email,
        "password": req.password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code != 200:
        error_msg = data.get("error", {}).get("message", "Đăng nhập thất bại")
        raise HTTPException(status_code=400, detail=error_msg)

    return {
        "status": "success",
        "email": data["email"],
        "user_id": data["localId"]
    }
@app.get("/")
def read_root():
    return {"message": "Xin chào đến với Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Tin nhắn trống")
    
    save_chat_message(req.user_id, "user", req.message)

    try:
        response = model.generate_content(req.message)
        bot_response = response.text
    except Exception as e:
        bot_response = "Bot đang bận, thử lại sau"

    save_chat_message(req.user_id, "bot", bot_response)
    return {"reply": bot_response}

@app.get("/history/{user_id}")
def history_endpoint(user_id: str):
    return {"history": get_chat_history(user_id)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)