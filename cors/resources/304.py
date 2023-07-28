# A header used to correlate requests and responses
state_header = b"content-language"

# Static ETag to use (and expect)
etag = b"abcdef"

def error(msg):
    return (299, u"Client Error"), [
        (b'content-type', b'text/plain'),
        (b'access-control-allow-origin', b"*"),
        (b'access-control-expose-headers', state_header),
        (b'cache-control', b'no-store')
    ], msg

def main(request, response):
    headers = []

    inm = request.headers.get(b'if-none-match', None)
    raw_req_num = request.headers.get(state_header, None)
    if raw_req_num is None:
        return error(u"no req_num header in request")
    req_num = int(raw_req_num)
    if req_num > 8:
        return error(f"req_num {req_num} out of range")

    headers.extend(
        (
            (b"Access-Control-Expose-Headers", state_header),
            (state_header, req_num),
            (b"A", req_num),
            (b"B", req_num),
        )
    )
    if req_num % 2:  # odd requests are the first in a test pair
        if inm:
            # what are you doing here? This should be a fresh request.
            return error(u"If-None-Match on first request")
        status = 200, b"OK"
        headers.extend(
            (
                (b"Access-Control-Allow-Origin", b"*"),
                (b"Content-Type", b"text/plain"),
                (b"Cache-Control", b"private, max-age=3, must-revalidate"),
                (b"ETag", etag),
            )
        )
        return status, headers, b"Success"
    else:  # even requests are the second in a pair, and should have a good INM.
        if inm != etag:
            # Bad browser.
            return (
                error(u"If-None-Match missing")
                if inm is None
                else error(u"If-None-Match '%s' mismatches")
            )
        if req_num == 4:
            headers.append((b"Access-Control-Expose-Headers", b"a, b"))
        elif req_num == 6:
            headers.append((b"Access-Control-Expose-Headers", b"a"))
        elif req_num == 8:
            headers.append((b"Access-Control-Allow-Origin", b"other.origin.example:80"))
        status = 304, b"Not Modified"
        return status, headers, b""
