import json
from cookies.resources import helpers

from wptserve.utils import isomorphic_decode

def main(request, response):
    headers = helpers.setNoCacheAndCORSHeaders(request, response)
    headers[0] = (b"Content-Type", b"text/javascript")
    cookies = helpers.readCookies(request)
    decoded_cookies = {isomorphic_decode(key): isomorphic_decode(val) for key, val in cookies.items()}
    return (
        headers,
        f"""self._cookies = [{', '.join([f'"{name}"' for name in decoded_cookies])}];\n""",
    )
