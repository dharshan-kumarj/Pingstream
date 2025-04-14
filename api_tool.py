import streamlit as st
import subprocess
import json
import tempfile
import os
import uuid
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
    .collection-folder {
        background-color: #e6f0ff;
        border-radius: 4px;
        padding: 8px;
        margin-bottom: 5px;
        cursor: pointer;
    }
    .collection-request {
        padding: 5px 10px;
        margin-left: 15px;
        border-left: 2px solid #ccc;
        margin-bottom: 5px;
        cursor: pointer;
    }
    .collection-request:hover {
        background-color: #f0f2f6;
        border-left: 2px solid #4a90e2;
    }
</style>
""", unsafe_allow_html=True)

def parse_openapi_spec(data):
    """Parse OpenAPI specification to extract endpoints"""
    collections = []
    
    # Check if it's OpenAPI format
    if 'openapi' in data and 'paths' in data:
        # Process OpenAPI spec
        for path, path_data in data['paths'].items():
            for method, operation in path_data.items():
                if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                    # Get tag as folder name (if exists)
                    folder = 'Default'
                    if 'tags' in operation and operation['tags']:
                        folder = operation['tags'][0]
                    
                    # Get summary/description
                    name = operation.get('summary', path)
                    if not name or name == path:
                        name = operation.get('operationId', path)
                    
                    # Extract parameters
                    params = []
                    if 'parameters' in operation:
                        for param in operation['parameters']:
                            if param['in'] == 'query':
                                params.append({
                                    "key": param['name'],
                                    "value": ""
                                })
                    
                    # Extract request body schema if exists
                    body = "{}"
                    if 'requestBody' in operation and 'content' in operation['requestBody']:
                        if 'application/json' in operation['requestBody']['content']:
                            schema = operation['requestBody']['content']['application/json'].get('schema', {})
                            # Generate a sample body based on schema (simplified)
                            if 'properties' in schema:
                                sample_body = {}
                                for prop, details in schema['properties'].items():
                                    sample_body[prop] = ""
                                body = json.dumps(sample_body, indent=2)
                    
                    # Extract headers
                    headers = []
                    if 'parameters' in operation:
                        for param in operation['parameters']:
                            if param['in'] == 'header':
                                headers.append({
                                    "key": param['name'],
                                    "value": ""
                                })
                    
                    # Create request object
                    request = {
                        "id": str(uuid.uuid4()),
                        "name": name,
                        "method": method.upper(),
                        "url": path,
                        "headers": headers,
                        "params": params,
                        "body": body
                    }
                    
                    # Add to collections
                    found = False
                    for collection in collections:
                        if collection['name'] == folder:
                            collection['requests'].append(request)
                            found = True
                            break
                    
                    if not found:
                        collections.append({
                            "name": folder,
                            "requests": [request]
                        })
    
    # Check if it's a Postman collection
    elif 'info' in data and 'item' in data:
        def process_items(items, parent_name=None):
            for item in items:
                if 'request' in item:
                    # This is a request
                    folder = parent_name or 'Default'
                    
                    # Extract URL
                    url = ""
                    if isinstance(item['request']['url'], dict):
                        url = item['request']['url'].get('raw', '')
                    else:
                        url = item['request']['url']
                    
                    # Extract headers
                    headers = []
                    if 'header' in item['request']:
                        for header in item['request']['header']:
                            headers.append({
                                "key": header['key'],
                                "value": header.get('value', '')
                            })
                    
                    # Extract body
                    body = "{}"
                    if 'body' in item['request'] and item['request']['body']:
                        if 'raw' in item['request']['body']:
                            body = item['request']['body']['raw']
                    
                    # Create request object
                    request = {
                        "id": str(uuid.uuid4()),
                        "name": item['name'],
                        "method": item['request']['method'],
                        "url": url,
                        "headers": headers,
                        "params": [],  # Postman stores params in the URL
                        "body": body
                    }
                    
                    # Add to collections
                    found = False
                    for collection in collections:
                        if collection['name'] == folder:
                            collection['requests'].append(request)
                            found = True
                            break
                    
                    if not found:
                        collections.append({
                            "name": folder,
                            "requests": [request]
                        })
                        
                elif 'item' in item:
                    # This is a folder
                    process_items(item['item'], item['name'])
            
        process_items(data['item'])
    
    return collections

def load_request(request_data):
    """Load request data into the form"""
    st.session_state.method = request_data['method']
    st.session_state.url = request_data['url']
    st.session_state.headers = request_data['headers'] if request_data['headers'] else [{"key": "", "value": ""}]
    st.session_state.params = request_data['params'] if request_data['params'] else [{"key": "", "value": ""}]
    st.session_state.body = request_data['body']

def main():
    st.title("🚀 Lightweight API Tester")
    
    # Initialize session state variables
    if 'collections' not in st.session_state:
        st.session_state.collections = []
    if 'expanded_folders' not in st.session_state:
        st.session_state.expanded_folders = set()
    if 'headers' not in st.session_state:
        st.session_state.headers = [{"key": "", "value": ""}]
    if 'params' not in st.session_state:
        st.session_state.params = [{"key": "", "value": ""}]
    if 'body' not in st.session_state:
        st.session_state.body = '{}'
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    with st.sidebar:
        st.subheader("Import API Collection")
        
        # File uploader for API collections
        uploaded_file = st.file_uploader("Upload OpenAPI or Collection JSON", type=["json", "yaml"])
        
        if uploaded_file is not None:
            try:
                # Parse the uploaded file
                content = uploaded_file.read()
                if uploaded_file.type == "application/x-yaml" or uploaded_file.name.endswith('.yaml'):
                    import yaml
                    data = yaml.safe_load(content)
                else:
                    data = json.loads(content)
                
                if st.button("Process Collection"):
                    with st.spinner('Processing collection...'):
                        collections = parse_openapi_spec(data)
                        if collections:
                            st.success(f"Successfully imported {sum(len(c['requests']) for c in collections)} endpoints in {len(collections)} folders")
                            # Give collection a name based on the file name
                            collection_name = uploaded_file.name.split('.')[0]
                            # Add the new collection to the existing ones
                            for collection in collections:
                                collection_existing = False
                                for existing_collection in st.session_state.collections:
                                    if existing_collection['name'] == collection['name']:
                                        # Merge requests
                                        existing_collection['requests'].extend(collection['requests'])
                                        collection_existing = True
                                if not collection_existing:
                                    st.session_state.collections.append(collection)
                        else:
                            st.error("Failed to parse the collection. Make sure it's a valid OpenAPI or Postman collection.")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        
        # Clear collections button
        if st.session_state.collections and st.button("Clear All Collections"):
            st.session_state.collections = []
        
        # Display collections and endpoints
        if st.session_state.collections:
            st.subheader("API Collections")
            
            for collection_idx, collection in enumerate(st.session_state.collections):
                # Display folder
                if st.button(f"📁 {collection['name']}", key=f"folder_{collection_idx}"):
                    if collection['name'] in st.session_state.expanded_folders:
                        st.session_state.expanded_folders.remove(collection['name'])
                    else:
                        st.session_state.expanded_folders.add(collection['name'])
                
                # Display requests if folder is expanded
                if collection['name'] in st.session_state.expanded_folders:
                    for req_idx, request in enumerate(collection['requests']):
                        # Display request with method color
                        method_colors = {
                            'GET': 'green',
                            'POST': 'blue',
                            'PUT': 'orange',
                            'DELETE': 'red',
                            'PATCH': 'purple'
                        }
                        method_color = method_colors.get(request['method'], 'gray')
                        request_label = f"<span style='color:{method_color};font-weight:bold;'>{request['method']}</span> {request['name']}"
                        
                        if st.button(request_label, key=f"req_{collection_idx}_{req_idx}", use_container_width=True, help=request['url']):
                            load_request(request)
        
        # Regular request history
        st.subheader("Request History")
        if st.session_state.history:
            for i, (timestamp, method, url) in enumerate(st.session_state.history):
                if st.button(f"{timestamp} - {method} {url[:30]}...", key=f"hist_{i}"):
                    # Functionality to load past requests could be added here
                    pass
    
    # Request Method and URL
    col1, col2 = st.columns([1, 4])
    with col1:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"], key="method")
    with col2:
        url = st.text_input("URL", placeholder="https://api.example.com/v1/resource", key="url")
    
    # Tabs for different request components
    tabs = st.tabs(["Headers", "Params", "Body", "Files"])
    
    # Headers Tab
    with tabs[0]:
        st.subheader("Headers")
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
        if method in ["POST", "PUT", "PATCH"] and body_type == "raw JSON" and st.session_state.body.strip():
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

    # Export Collection Button (at the bottom)
    if st.session_state.collections:
        if st.button("Export All Collections"):
            export_data = {
                "info": {
                    "name": "Exported API Collection",
                    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
                },
                "item": []
            }
            
            for collection in st.session_state.collections:
                folder = {
                    "name": collection["name"],
                    "item": []
                }
                
                for request in collection["requests"]:
                    req_item = {
                        "name": request["name"],
                        "request": {
                            "method": request["method"],
                            "url": request["url"],
                            "header": [{"key": h["key"], "value": h["value"]} for h in request["headers"] if h["key"]],
                            "body": {
                                "mode": "raw",
                                "raw": request["body"],
                                "options": {
                                    "raw": {
                                        "language": "json"
                                    }
                                }
                            }
                        }
                    }
                    folder["item"].append(req_item)
                
                export_data["item"].append(folder)
            
            # Convert to JSON
            export_json = json.dumps(export_data, indent=2)
            
            # Display download link
            st.download_button(
                label="Download Collection",
                data=export_json,
                file_name="api_collection.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()