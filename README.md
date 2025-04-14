# Lightweight API Tester



## Overview

Lightweight API Tester is a minimalist, resource-efficient GUI tool for testing REST APIs. Built with Python and Streamlit, it provides a clean interface for making API requests without the memory overhead of tools like Postman, making it perfect for development environments with limited resources.

## Features

- 🚀 **Lightweight** - Optimized for systems with limited RAM
- 🔄 **Core HTTP Methods** - Support for GET, POST, PUT, DELETE
- 📝 **Request Builder** - Easily construct complete API requests
- 🧩 **Header Management** - Add, edit, and remove custom headers
- 📊 **Parameter Builder** - Construct query parameters with a clean interface
- 📦 **JSON Body Editor** - With built-in JSON validation
- 📁 **File Upload** - Send files with your requests
- 📜 **Request History** - Track your recent API calls
- 💻 **Curl Integration** - Uses curl under the hood for reliable request handling

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- curl (must be installed on your system and available in PATH)

### Setup

1. Clone this repository or download the source code

2. Install the required dependencies:
   ```bash
   pip install streamlit
   ```

3. Run the application:
   ```bash
   streamlit run api_tool.py
   ```

## Usage Guide

### Making a Simple Request

1. Select the HTTP method (GET, POST, PUT, DELETE)
2. Enter the URL for your API endpoint
3. Click "Send Request"

### Adding Headers

1. Navigate to the "Headers" tab
2. Enter key-value pairs for your headers
3. Click "Add Header" for additional headers

### Adding Query Parameters

1. Navigate to the "Params" tab
2. Enter key-value pairs for query parameters
3. Click "Add Parameter" for additional parameters

### Sending a JSON Body

1. Navigate to the "Body" tab
2. Select "raw JSON" as the body type
3. Enter your JSON in the text area (validation is automatic)

### Uploading Files

1. Navigate to the "Files" tab
2. Use the file uploader to select your file
3. The file will be included in your request

## Troubleshooting

### ScriptRunContext Warnings

If you see warnings about "missing ScriptRunContext", you can safely ignore them or suppress them by adding this flag when running:

```bash
streamlit run api_tester.py --logger.level=error
```

Alternatively, create a `.streamlit/config.toml` file with:
```
[logger]
level = "error"
```

### Request Errors

- Verify that curl is properly installed on your system
- Check your internet connection
- Ensure the API endpoint URL is correct
- Validate your JSON body for proper formatting

## Screenshots

*[Add screenshots of your application here]*

## Requirements

- Python 3.7+
- Streamlit
- curl


## Created By

Developed by dharshan-kumarj on April 13, 2025.

---

💻 **Optimized for low-resource environments (4GB RAM systems)**