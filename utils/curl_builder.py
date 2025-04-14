def build_curl_command(method, url, headers, params, body, uploaded_file):
    curl_cmd = ["curl", "-s"]

    if method != "GET":
        curl_cmd.extend(["-X", method])

    for header in headers:
        if header["key"] and header["value"]:
            curl_cmd.extend(["-H", f"{header['key']}: {header['value']}"])

    if method in ["POST", "PUT"] and body:
        curl_cmd.extend(["-H", "Content-Type: application/json"])
        curl_cmd.extend(["-d", body])

    if uploaded_file:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            file_path = tmp_file.name
        curl_cmd.extend(["-F", f"file=@{file_path}"])

    if params:
        query = "&".join(f"{p['key']}={p['value']}" for p in params if p["key"] and p["value"])
        if "?" in url:
            url += "&" + query
        elif query:
            url += "?" + query

    curl_cmd.append(url)
    return curl_cmd
