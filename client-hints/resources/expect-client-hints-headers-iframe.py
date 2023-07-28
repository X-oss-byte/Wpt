from wptserve.utils import isomorphic_decode

import importlib
client_hints_list = importlib.import_module("client-hints.resources.clienthintslist").client_hints_list

def main(request, response):
    """
    Simple handler that returns an HTML response that passes when the required
    Client Hints are received as request headers.
    """

    result = u"PASS"
    log = u""
    for value in client_hints_list():
        should = (request.GET[value.lower()] == b"true")
        present = request.headers.get(value.lower()) or request.headers.get(value)
        if present:
            log += f"{isomorphic_decode(value)} {str(should)} {isomorphic_decode(present)}, "
        else:
            log += f"{isomorphic_decode(value)} {str(should)} {str(present)}, "
        if (should and not present) or (not should and present):
            if present:
                result = f"FAIL {isomorphic_decode(value)} {str(should)} {isomorphic_decode(present)}"
            else:
                result = f"FAIL {isomorphic_decode(value)} {str(should)} {str(present)}"
            break

    response.headers.append(b"Access-Control-Allow-Origin", b"*")
    body = u"<script>console.log('" + log + u"'); window.parent.postMessage('" + result + u"', '*');</script>"

    response.content = body
