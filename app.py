import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk", page_icon="🧵")
st.title("🧵 TailorTalk - Calendar Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    role = "🧑‍💻 You" if msg["role"] == "user" else "🤖 TailorTalk"
    st.markdown(f"**{role}:** {msg['content']}")

# Input box
user_input = st.text_input("What would you like to do?", key="input")

# On submit
if st.button("Send"):
    if user_input:
        # Save user input
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("TailorTalk is thinking..."):
            try:
                res = requests.post("http://127.0.0.1:8000/chat", json={"message": user_input})
                if res.status_code == 200:
                    bot_reply = res.json()["reply"]
                    st.session_state.messages.append({"role": "bot", "content": bot_reply})
                else:
                    st.session_state.messages.append({"role": "bot", "content": "❌ API error!"})
            except:
                st.session_state.messages.append({"role": "bot", "content": "🚫 Backend not running!"})

        st.rerun()
