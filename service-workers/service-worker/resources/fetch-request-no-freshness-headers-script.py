def main(request, response):
    headers = [(b"ETag", b"abc123"), (b"Content-Type", b"text/javascript")]
    return headers, b"/* empty script */"
