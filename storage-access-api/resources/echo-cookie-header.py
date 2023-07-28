def main(request, response):
  # Set the cors enabled headers.
  origin = request.headers.get(b"Origin")
  headers = []
  if origin is not None and origin != b"null":
    headers.extend((
        (b"Content-Type", b"text/plain"),
        (b"Access-Control-Allow-Origin", origin),
        (b"Access-Control-Allow-Credentials", 'true'),
    ))
  cookie_header = request.headers.get(b"Cookie", b"")

  return (200, headers, cookie_header)
