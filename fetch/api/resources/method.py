from wptserve.utils import isomorphic_encode

def main(request, response):
    headers = []
    if b"cors" in request.GET:
        headers.extend(
            (
                (b"Access-Control-Allow-Origin", b"*"),
                (b"Access-Control-Allow-Credentials", b"true"),
                (b"Access-Control-Allow-Methods", b"GET, POST, PUT, FOO"),
                (b"Access-Control-Allow-Headers", b"x-test, x-foo"),
                (b"Access-Control-Expose-Headers", b"x-request-method"),
            )
        )
    headers.extend(
        (
            (b"x-request-method", isomorphic_encode(request.method)),
            (
                b"x-request-content-type",
                request.headers.get(b"Content-Type", b"NO"),
            ),
            (
                b"x-request-content-length",
                request.headers.get(b"Content-Length", b"NO"),
            ),
            (
                b"x-request-content-encoding",
                request.headers.get(b"Content-Encoding", b"NO"),
            ),
            (
                b"x-request-content-language",
                request.headers.get(b"Content-Language", b"NO"),
            ),
            (
                b"x-request-content-location",
                request.headers.get(b"Content-Location", b"NO"),
            ),
        )
    )
    return headers, request.body
