import streamlit as st
import json
import os

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def render_history():
    with st.sidebar:
        st.subheader("Request History")
        if 'history' not in st.session_state:
            st.session_state.history = load_history()

        for i, entry in enumerate(st.session_state.history):
            timestamp, method, url = entry
            if st.button(f"{timestamp} - {method} {url[:30]}...", key=f"hist_{i}"):
                st.session_state.url = url
                st.session_state.method = method
                # You could also load headers/body if saving those later

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            save_history([])
