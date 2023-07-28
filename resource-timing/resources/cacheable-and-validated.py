def main(request, response):
    if tao := request.GET.get(b'timing_allow_origin'):
        response.headers.set(b"Timing-Allow-Origin", tao)

    if b'origin' in request.headers:
      origin = request.headers[b'origin']
      response.headers.set(b'Access-Control-Allow-Origin', origin)

    content = request.GET.first(b'content')
    response.headers.set(b'Cache-Control', b'max-age=60')
    response.headers.set(b'ETag', b'assdfsdfe')

    # Handle CORS-preflights of non-simple requests.
    if request.method == 'OPTIONS':
        response.status = 204
        if requested_method := request.headers.get(
            b"Access-Control-Request-Method"
        ):
            response.headers.set(b"Access-Control-Allow-Methods", requested_method)
        if requested_headers := request.headers.get(
            b"Access-Control-Request-Headers"
        ):
            response.headers.set(b"Access-Control-Allow-Headers", requested_headers)
    elif 'Cache-Control' in request.headers:
        response.status = (304, b'NotModified')
    else:
        response.status = (200, b'OK')
        response.write_status_headers()
        response.writer.write(content)
