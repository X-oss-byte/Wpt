def main(request, response):
    type = request.GET.first(b"type", None)
    subtype = request.GET.first(b"subtype", None)
    if type and subtype:
        response.headers[b"Content-Type"] = type + b"/" + subtype

    if removeContentType := request.GET.first(b"removeContentType", None):
        try:
            del response.headers[b"Content-Type"]
        except KeyError:
            pass

    content = b'<head>'
    if mimeHead := request.GET.first(b"mime", None):
        content += b'<meta http-equiv="Content-Type" content="%s; charset=utf-8"/>' % mimeHead
    content += b"</head>"

    return content
