import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Chatbot", layout="wide")

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.is_logged_in:
    st.title("🔐 Đăng nhập hệ thống")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        btn_login = st.form_submit_button("Đăng nhập")

        if btn_login:
            try:
                res = requests.post(
                    f"{BACKEND_URL}/auth/login",
                    json={"email": email, "password": password},
                    timeout=5
                )
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.is_logged_in = True
                    st.session_state.user_email = data["email"]
                    st.session_state.user_id = data["user_id"]

                    hist_res = requests.get(
                        f"{BACKEND_URL}/history/{data['user_id']}",
                        timeout=5
                    )
                    if hist_res.status_code == 200:
                        st.session_state.messages = hist_res.json().get("history", [])
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error(res.text)
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")

else:
    st.sidebar.title("👤 Thành viên")
    st.sidebar.info(f"Đang đăng nhập:\n{st.session_state.user_email}")

    if st.sidebar.button("Đăng xuất"):
        st.session_state.clear()
        st.rerun()

    st.title("🤖 AI Chatbot")

    for msg in st.session_state.messages:
        role = "assistant" if msg["role"] == "bot" else "user"
        with st.chat_message(role):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi..."):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Đang suy nghĩ..."):
                try:
                    chat_res = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={
                            "user_id": st.session_state.user_id,
                            "message": prompt
                        },
                        timeout=60
                    )
                    if chat_res.status_code == 200:
                        reply = chat_res.json()["reply"]
                        st.markdown(reply)
                        st.session_state.messages.append({
                            "role": "bot",
                            "content": reply
                        })
                    else:
                        st.error(chat_res.text)
                except Exception as e:
                    st.error(f"Lỗi kết nối: {e}")