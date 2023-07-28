from wptserve.utils import isomorphic_decode

def main(request, response):
    headers = [(b"Content-Type", b"application/json"),
               (b"Access-Control-Allow-Credentials", b"true")]

    if b"origin" in request.headers:
        headers.append((b"Access-Control-Allow-Origin", request.headers[b"origin"]))

    values = []
    for key in request.cookies:
        values.extend(
            u"\"%s\": \"%s\"" % (isomorphic_decode(key), value)
            for value in request.cookies.get_list(key)
        )
    body = u"{ %s }" % u",".join(values)
    return headers, body
