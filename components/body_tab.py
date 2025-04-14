import streamlit as st
import json

def body_tab(tab):
    with tab:
        st.subheader("Request Body")
        body_type = st.radio("Body Type", ["none", "raw JSON"], horizontal=True)

        if body_type == "raw JSON":
            if 'body' not in st.session_state:
                st.session_state.body = '{}'
            body_json = st.text_area("JSON Body", st.session_state.body, height=200)
            try:
                if body_json:
                    json.loads(body_json)
                st.session_state.body = body_json
            except json.JSONDecodeError:
                st.error("Invalid JSON format")

        return st.session_state.body if body_type == "raw JSON" else None
