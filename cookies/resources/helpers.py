from urllib.parse import parse_qs

from wptserve.utils import isomorphic_encode

def setNoCacheAndCORSHeaders(request, response):
    """Set Cache-Control, CORS and Content-Type headers appropriate for the cookie tests."""
    origin = request.headers[b"origin"] if b"origin" in request.headers else b"*"
    headers = [
        (b"Content-Type", b"application/json"),
        (b"Access-Control-Allow-Credentials", b"true"),
        *(
            (b"Access-Control-Allow-Origin", origin),
            (b"Cache-Control", b"no-cache"),
            (b"Expires", b"Fri, 01 Jan 1990 00:00:00 GMT"),
        ),
    ]
    return headers

def makeCookieHeader(name, value, otherAttrs):
    """Make a Set-Cookie header for a cookie with the name, value and attributes provided."""
    def makeAV(a, v):
        if None == v or b"" == v:
            return a
        return b"%s=%i" % (a, v) if isinstance(v, int) else b"%s=%s" % (a, v)

    # ensure cookie name is always first
    attrs = [b"%s=%s" % (name, value)]
    attrs.extend(makeAV(a, v) for (a, v) in otherAttrs.items())
    return (b"Set-Cookie", b"; ".join((attrs)))

def makeDropCookie(name, secure):
    attrs = {b"max-age": 0, b"path": b"/"}
    if secure:
        attrs[b"secure"] = b""
    return makeCookieHeader(name, b"", attrs)

def readParameter(request, paramName, requireValue):
    """Read a parameter from the request. Raise if requireValue is set and the
    parameter has an empty value or is not present."""
    params = parse_qs(request.url_parts.query)
    param = params[paramName][0].strip()
    if len(param) == 0:
        raise Exception(u"Empty or missing name parameter.")
    return isomorphic_encode(param)

def readCookies(request):
    """Read the cookies from the client present in the request."""
    cookies = {}
    for key in request.cookies:
        for cookie in request.cookies.get_list(key):
            # do we care we'll clobber cookies here? If so, do we
            # need to modify the test to take cookie names and value lists?
            cookies[key] = cookie.value
    return cookies
