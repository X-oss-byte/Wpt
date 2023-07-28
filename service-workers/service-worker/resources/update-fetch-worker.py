import random
import time

def main(request, response):
    content_type = b''
    extra_body = u''

    content_type = b'application/javascript'
    headers = [
        (b'Cache-Control', b'no-cache, must-revalidate'),
        (b'Pragma', b'no-cache'),
        (b'Content-Type', content_type),
    ]
    extra_body = u"self.onfetch = (event) => { event.respondWith(fetch(event.request)); };"

    # Return a different script for each access.
    return headers, f'/* {time.time()} {random.random()} */ {extra_body}'
