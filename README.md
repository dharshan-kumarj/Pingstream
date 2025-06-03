# 🚀 Pingstream — The Lightweight API Tester

**Pingstream** is a minimalist, memory-efficient GUI tool for testing REST APIs. Built using Python, Streamlit, and `curl`, it’s perfect for developers working in low-resource environments (like 4GB RAM machines) where heavy tools like Postman just don't cut it.

---

## 🔧 Features

* ⚡ **Lightweight** – Ideal for systems with limited RAM
* 🔄 **Core HTTP Methods** – GET, POST, PUT, DELETE
* 🧱 **Request Builder** – Build complete API calls with ease
* 🧩 **Header Manager** – Add, edit, and remove custom headers
* 🧮 **Query Parameter Support** – Clean interface for managing query params
* 📦 **JSON Body Editor** – Includes automatic JSON validation
* 📁 **File Upload** – Send files with your API requests
* 🕓 **Request History** – View your recent API calls
* 🌀 **Curl-based Engine** – Reliable, fast request handling
* 📤 **Import/Export** – Supports Postman collections and OpenAPI JSON files

---

## 📥 Installation

### ✅ Prerequisites

* Python 3.7+
* `pip`
* `curl` (should be installed and accessible in your system PATH)

### 🛠 Setup

```bash
# Clone or download this repo
git clone https://github.com/yourusername/pingstream.git
cd pingstream

# Install dependencies
pip install streamlit

# Run the app
streamlit run pingstream.py
```

---

## 🚀 Usage Guide

### 🔹 Make a Request

1. Select HTTP method (GET, POST, etc.)
2. Enter the API URL
3. Click "Send Request"

### 🔹 Manage Headers

* Go to the "Headers" tab
* Add key-value pairs
* Click "Add Header" as needed

### 🔹 Add Query Params

* Go to the "Params" tab
* Add key-value pairs
* Click "Add Parameter"

### 🔹 Send JSON Body

* Go to the "Body" tab
* Choose “raw JSON”
* Paste your JSON (automatic validation included)

### 🔹 Upload Files

* Go to the "Files" tab
* Use the uploader to include your file in the request

### 🔹 Import/Export

* Import API definitions from Postman or OpenAPI JSON
* Export your requests for reuse or sharing

---

## 🧰 Troubleshooting

### ⚠ ScriptRunContext Warnings

If you see warnings like `missing ScriptRunContext`, you can suppress them with:

```bash
streamlit run pingstream.py --logger.level=error
```

Or create a config file:

```toml
# .streamlit/config.toml
[logger]
level = "error"
```

### ❌ Request Errors

* Confirm `curl` is installed: `curl --version`
* Check your internet and API endpoint
* Validate your JSON structure

---

## 🧾 Requirements

* Python 3.7+
* Streamlit
* curl

---


## 👨‍💻 Created By

**Pingstream** was developed by [@dharshan-kumarj](https://github.com/dharshan-kumarj) on April 13, 2025, with love for developers using low-end machines.

**UI Enhancements by** [@ronnie-allen](https://github.com/ronnie-allen) — improving the design and experience of the Streamlit interface.

> 💡 Built on Linux, powered by `curl`, and designed to work even when your RAM says “no”.

---



