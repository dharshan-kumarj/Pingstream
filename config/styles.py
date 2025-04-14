import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: #f0f2f6;
            border-radius: 4px 4px 0 0;
            padding: 10px 16px;
            font-size: 14px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff;
            border-bottom: 2px solid #4a90e2;
        }
        .response-area {
            background-color: #f0f2f6;
            border-radius: 5px;
            padding: 15px;
        }
        .url-input {
            background-color: white;
            border-radius: 5px;
            padding: 8px;
        }
    </style>
    """, unsafe_allow_html=True)
