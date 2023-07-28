import re

def main(request, response):
    key = request.GET[b'id']
    action = request.GET[b'action']
    if action == b'put':
        # We want the raw input for 'q'
        q = re.search(r'q=([^&]+)', request.url_parts.query).groups()[0]
        request.server.stash.put(key, q)
        return [(b"Content-Type", b"text/html")], f'Put {q}'
    else:
        q = request.server.stash.take(key)
        return ([(b"Content-Type", b"text/html")], q) if q != None else ([], u"")
