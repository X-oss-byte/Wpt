def main(request, response):
    headers = []

    if b"ACAOrigin" in request.GET:
        headers.extend(
            (b"Access-Control-Allow-Origin", item)
            for item in request.GET[b"ACAOrigin"].split(b",")
        )
    return headers, b"{ \"result\": \"success\" }"
