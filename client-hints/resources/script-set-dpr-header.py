def main(request, response):
    headers = [(b"Content-Type", b"text/javascript")]
    body = f"""dprHeader = "{request.headers.get(b'sec-ch-dpr', '')}";"""
    return 200, headers, body
