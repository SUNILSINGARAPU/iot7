import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# -------------------------------
# Firebase Configuration
# -------------------------------
if not firebase_admin._apps:
    # Replace with your downloaded JSON key path
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://your-project-id.firebaseio.com/"
    })

# Reference to a database path
ref = db.reference("messages")

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("💬 Firebase Realtime Database Demo with Streamlit")

# Input form
st.subheader("Send a Message")
user = st.text_input("Your Name", "")
message = st.text_area("Message", "")
if st.button("Send"):
    if user and message:
        new_msg = {
            "user": user,
            "message": message,
            "timestamp": int(time.time())
        }
        ref.push(new_msg)
        st.success("Message sent!")
    else:
        st.warning("Please fill out both fields.")

# -------------------------------
# Live Message Stream
# -------------------------------
st.subheader("📡 Live Messages")

# Function to get messages ordered by timestamp
def get_messages():
    messages = ref.order_by_child("timestamp").get()
    if messages:
        # Convert dict to list and sort by time
        sorted_msgs = sorted(messages.items(), key=lambda x: x[1]["timestamp"], reverse=True)
        return sorted_msgs
    return []

# Auto-refresh messages every few seconds
placeholder = st.empty()

while True:
    with placeholder.container():
        messages = get_messages()
        if messages:
            for key, msg in messages:
                st.markdown(f"**{msg['user']}**: {msg['message']}  \n🕒 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg['timestamp']))}")
        else:
            st.info("No messages yet. Start chatting!")
    time.sleep(5)
