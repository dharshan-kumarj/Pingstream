import subprocess
import tempfile
import json
import time
import os

def execute_curl_request(method, url, headers, params, body, uploaded_file):
    curl_cmd = ["curl", "-s", "-w", "%{http_code}"]  # -w for status code

    if method != "GET":
        curl_cmd += ["-X", method]

    for header in headers:
        if header["key"] and header["value"]:
            curl_cmd += ["-H", f"{header['key']}: {header['value']}"]

    if method in ["POST", "PUT"] and body:
        curl_cmd += ["-H", "Content-Type: application/json"]
        curl_cmd += ["-d", body]

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp:
            tmp.write(uploaded_file.getvalue())
            file_path = tmp.name
        curl_cmd += ["-F", f"file=@{file_path}"]
    else:
        file_path = None

    if params:
        param_str = "&".join([f"{p['key']}={p['value']}" for p in params if p["key"] and p["value"]])
        if "?" in url:
            url += "&" + param_str
        else:
            url += "?" + param_str

    curl_cmd.append(url)

    start = time.time()
    process = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    end = time.time()

    if file_path:
        os.unlink(file_path)

    if stderr:
        return {"error": stderr.decode(), "status": None, "time_ms": None, "body": None}

    output = stdout.decode()
    status_code = output[-3:]
    body = output[:-3]

    return {
        "status": int(status_code),
        "body": body,
        "time_ms": int((end - start) * 1000),
        "error": None
    }
