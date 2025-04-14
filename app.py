import streamlit as st
import json
from datetime import datetime

from config.styles import apply_custom_styles
from components.history_sidebar import render_history, save_history
from components.request_input import get_method_url
from components.headers_tab import headers_tab
from components.params_tab import params_tab
from components.body_tab import body_tab
from components.files_tab import files_tab
from utils.curl_builder import build_curl_command
from utils.request_handler import execute_curl_request  # Handles actual request

# Setup
st.set_page_config(page_title="Lightweight API Tester", layout="wide")
apply_custom_styles()

def main():
    st.title("🚀 Lightweight API Tester")
    render_history()

    method, url = get_method_url()
    tabs = st.tabs(["Headers", "Params", "Body", "Files"])

    headers = headers_tab(tabs[0])
    params = params_tab(tabs[1])
    body = body_tab(tabs[2])
    uploaded_file = files_tab(tabs[3])

    # Handle button click
    if st.button("🚀 Send Request", type="primary"):
        if not url:
            st.error("URL is required")
            return

        # Save to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.history.append((timestamp, method, url))
        save_history(st.session_state.history)

        # Build curl and execute
        curl_cmd = build_curl_command(method, url, headers, params, body, uploaded_file)
        st.session_state["curl_cmd"] = curl_cmd
        response = execute_curl_request(method, url, headers, params, body, uploaded_file)
        st.session_state["response"] = response

    # Show CURL command if available
    if "curl_cmd" in st.session_state:
        st.subheader("📋 CURL Command")
        st.code(" ".join(st.session_state["curl_cmd"]), language="bash")

    # Show response if available
    if "response" in st.session_state and st.session_state["response"]:
        response = st.session_state["response"]

        if response["error"]:
            st.error(f"Error: {response['error']}")
        else:
            st.subheader("✅ Response")
            st.markdown(
                f"**Status Code:** `{response['status']}` &nbsp;&nbsp; ⏱️ **Time:** `{response['time_ms']} ms`"
            )

            view_mode = st.radio("View As", ["Pretty", "Raw", "Download"], horizontal=True)

            if view_mode == "Pretty":
                try:
                    parsed = json.loads(response["body"])
                    st.json(parsed)
                except json.JSONDecodeError:
                    st.warning("Response is not valid JSON.")
                    st.text_area("Raw Response", response["body"], height=300)

            elif view_mode == "Raw":
                st.text_area("Raw Response", response["body"], height=300)

            elif view_mode == "Download":
                st.download_button("📥 Download Response", response["body"], file_name="response.json", mime="application/json")

if __name__ == "__main__":
    main()
