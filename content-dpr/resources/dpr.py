from wptserve.utils import isomorphic_decode

def main(request, response):
    """
    Simple handler that sets a response header based on which client hint
    request headers were received.
    """

    response.headers.append(b"Access-Control-Allow-Origin", b"*")
    values = request.GET
    name = values.first(b'name')
    type = values.first(b'mimeType')
    dpr = values.first(b'dpr')
    double = values.first(b'double') if b'double' in values else None
    image_path = request.doc_root + u"/".join(request.url_parts[2].split(u"/")[:-1]) + u"/" + isomorphic_decode(name)
    with open(image_path, "rb") as f:
        buff = f.read()
    response.headers.set(b"Content-Type", type)
    response.headers.set(b"Content-DPR", dpr)
    if double:
        response.headers.append(b"Content-DPR", double)
    response.headers.set(b"Content-Length", len(buff))
    response.content = buff
