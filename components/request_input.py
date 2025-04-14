import streamlit as st

def get_method_url():
    col1, col2 = st.columns([1, 4])
    with col1:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE"], key="method")
    with col2:
        url = st.text_input("URL", placeholder="https://api.example.com/v1/resource", key="url")
    return method, url
