import streamlit as st
import subprocess
import json
import os

def execute_request(curl_cmd, uploaded_file=None):
    with st.spinner("Executing request..."):
        try:
            process = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if uploaded_file:
                uploaded_file.close()
                os.unlink(uploaded_file.name)

            if stderr:
                st.error(f"Error: {stderr.decode('utf-8')}")
                return

            response_text = stdout.decode('utf-8')
            st.subheader("📥 Response")

            # Toggle viewer
            view_mode = st.radio("View As", ["Pretty", "Raw", "Download"], horizontal=True)

            if view_mode == "Pretty":
                try:
                    response_json = json.loads(response_text)
                    st.json(response_json)
                except json.JSONDecodeError:
                    st.warning("Not a valid JSON response. Showing as text:")
                    st.text_area("Response", response_text, height=300)
            elif view_mode == "Raw":
                st.code(response_text, language="json")
            elif view_mode == "Download":
                st.download_button(
                    label="Download Response",
                    data=response_text,
                    file_name="response.json" if is_json(response_text) else "response.txt",
                    mime="application/json" if is_json(response_text) else "text/plain"
                )

        except Exception as e:
            st.error(f"Exception occurred: {str(e)}")

def is_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False
