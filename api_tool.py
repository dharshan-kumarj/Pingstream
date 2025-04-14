import streamlit as st
import subprocess
import json
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="Lightweight API Tester", layout="wide")

# Add custom CSS for a cleaner look
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
        white-space: pre-wrap;
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

def main():
    st.title("🚀 Lightweight API Tester")
    
    with st.sidebar:
        st.subheader("Request History")
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        if st.session_state.history:
            for i, (timestamp, method, url) in enumerate(st.session_state.history):
                if st.button(f"{timestamp} - {method} {url[:30]}...", key=f"hist_{i}"):
                    # Functionality to load past requests could be added here
                    pass
    
    # Request Method and URL
    col1, col2 = st.columns([1, 4])
    with col1:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE"], key="method")
    with col2:
        url = st.text_input("URL", placeholder="https://api.example.com/v1/resource", key="url")
    
    # Tabs for different request components
    tabs = st.tabs(["Headers", "Params", "Body", "Files"])
    
    # Headers Tab
    with tabs[0]:
        st.subheader("Headers")
        if 'headers' not in st.session_state:
            st.session_state.headers = [{"key": "", "value": ""}]
        
        for i, header in enumerate(st.session_state.headers):
            cols = st.columns([3, 3, 1])
            with cols[0]:
                key = st.text_input("Key", header["key"], key=f"header_key_{i}")
            with cols[1]:
                value = st.text_input("Value", header["value"], key=f"header_value_{i}")
            with cols[2]:
                if st.button("❌", key=f"del_header_{i}"):
                    st.session_state.headers.pop(i)
                    st.rerun()
            
            st.session_state.headers[i] = {"key": key, "value": value}
        
        if st.button("+ Add Header"):
            st.session_state.headers.append({"key": "", "value": ""})
            st.rerun()
    
    # Parameters Tab
    with tabs[1]:
        st.subheader("Query Parameters")
        if 'params' not in st.session_state:
            st.session_state.params = [{"key": "", "value": ""}]
        
        for i, param in enumerate(st.session_state.params):
            cols = st.columns([3, 3, 1])
            with cols[0]:
                key = st.text_input("Key", param["key"], key=f"param_key_{i}")
            with cols[1]:
                value = st.text_input("Value", param["value"], key=f"param_value_{i}")
            with cols[2]:
                if st.button("❌", key=f"del_param_{i}"):
                    st.session_state.params.pop(i)
                    st.rerun()
            
            st.session_state.params[i] = {"key": key, "value": value}
        
        if st.button("+ Add Parameter"):
            st.session_state.params.append({"key": "", "value": ""})
            st.rerun()
    
    # Body Tab
    with tabs[2]:
        st.subheader("Request Body")
        body_type = st.radio("Body Type", ["none", "raw JSON"], horizontal=True)
        
        if body_type == "raw JSON":
            if 'body' not in st.session_state:
                st.session_state.body = '{}'
            body_json = st.text_area("JSON Body", st.session_state.body, height=200)
            try:
                # Validate JSON
                if body_json:
                    json.loads(body_json)
                st.session_state.body = body_json
            except json.JSONDecodeError:
                st.error("Invalid JSON format")
    
    # Files Tab
    with tabs[3]:
        st.subheader("Files")
        uploaded_file = st.file_uploader("Upload File", type=None)
        if uploaded_file is not None:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "Size": uploaded_file.size}
            st.json(file_details)
    
    # Execute Request
    if st.button("🚀 Send Request", type="primary"):
        if not url:
            st.error("URL is required")
            return
        
        # Construct curl command
        curl_cmd = ["curl", "-s"]
        
        # Add method
        if method != "GET":
            curl_cmd.extend(["-X", method])
        
        # Add headers
        for header in st.session_state.headers:
            if header["key"] and header["value"]:
                curl_cmd.extend(["-H", f"{header['key']}: {header['value']}"])
        
        # Add JSON body
        if method in ["POST", "PUT"] and 'body' in st.session_state and st.session_state.body.strip():
            curl_cmd.extend(["-H", "Content-Type: application/json"])
            curl_cmd.extend(["-d", st.session_state.body])
        
        # Add file if uploaded
        if uploaded_file is not None:
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                file_path = tmp_file.name
            
            curl_cmd.extend(["-F", f"file=@{file_path}"])
        
        # Build URL with query parameters
        full_url = url
        if hasattr(st.session_state, 'params'):
            params = []
            for param in st.session_state.params:
                if param["key"] and param["value"]:
                    params.append(f"{param['key']}={param['value']}")
            
            if params:
                if "?" in url:
                    full_url += "&" + "&".join(params)
                else:
                    full_url += "?" + "&".join(params)
        
        curl_cmd.append(full_url)
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.history.append((timestamp, method, url))
        
        # Display the curl command
        st.code(" ".join(curl_cmd), language="bash")
        
        with st.spinner('Executing request...'):
            try:
                # Execute curl command
                process = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                # Remove temp file if created
                if 'file_path' in locals():
                    os.unlink(file_path)
                
                if stderr:
                    st.error(f"Error: {stderr.decode('utf-8')}")
                else:
                    response_text = stdout.decode('utf-8')
                    st.subheader("Response")
                    
                    # Display formatted response
                    try:
                        response_json = json.loads(response_text)
                        st.json(response_json)
                    except json.JSONDecodeError:
                        st.text_area("Response", response_text, height=300)
            
            except Exception as e:
                st.error(f"Error executing request: {str(e)}")

if __name__ == "__main__":
    main()