def main(request, response):
    headers = [(b"Access-Control-Allow-Origin", b"*")]
    return headers, b"{ \"result\": \"success\" }"
