import streamlit as st
import requests

# === Config ===
API_BASE = "http://localhost:8000"

st.set_page_config(page_title="🧠 Zoology Tutor Bot", layout="centered")
st.title("🧬 Zoology Tutor Chat Assistant")

# === Session State Init ===
if "jwt_token" not in st.session_state:
    try:
        res = requests.get(f"{API_BASE}/token")
        res.raise_for_status()
        st.session_state.jwt_token = res.json()["token"]
    except Exception as e:
        st.error(f"Token Error: {e}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# === Display Chat History ===
for msg in st.session_state.messages:
    with st.chat_message("user"):
        st.markdown(msg["user"])
    with st.chat_message("assistant"):
        st.markdown(msg["bot"])

# === Chat Input ===
user_query = st.chat_input("Ask something about Zoology or say 'generate quiz'...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)

    headers = {"Authorization": f"Bearer {st.session_state.jwt_token}"}
    try:
        response = requests.post(
            f"{API_BASE}/chat_agent",
            json={"query": user_query},
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        bot_reply = data["answer"]
    except Exception as e:
        bot_reply = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Save messages
    st.session_state.messages.append({
        "user": user_query,
        "bot": bot_reply
    })

# === Reset Session Button ===
if st.button("🔄 Reset Session"):
    try:
        res = requests.post(f"{API_BASE}/reset", headers={"Authorization": f"Bearer {st.session_state.jwt_token}"})
        res.raise_for_status()
        st.session_state.messages.clear()
        st.success("Session reset!")
        st.rerun()
    except Exception as e:
        st.error(f"Reset Error: {e}")
