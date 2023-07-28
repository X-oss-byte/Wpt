from wptserve.utils import isomorphic_decode

def main(request, response):
    status = int(request.GET[b"Status"]) if b'Status' in request.GET else 302
    url = isomorphic_decode(request.GET[b'Redirect'])
    headers = [(b"Location", url)]
    if b"ACAOrigin" in request.GET:
        headers.extend(
            (b"Access-Control-Allow-Origin", item)
            for item in request.GET[b"ACAOrigin"].split(b",")
        )
    for suffix in [b"Headers", b"Methods", b"Credentials"]:
        query = b"ACA%s" % suffix
        header = b"Access-Control-Allow-%s" % suffix
        if query in request.GET:
            headers.append((header, request.GET[query]))

    if b"ACEHeaders" in request.GET:
        headers.append((b"Access-Control-Expose-Headers", request.GET[b"ACEHeaders"]))

    return status, headers, b""
