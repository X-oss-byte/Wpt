def main(request, response):
    url = request.GET[b'url'] if b'url' in request.GET else b''
    return 301, [(b'Location', url),(b'Accept-CH', b'sec-ch-device-memory, device-memory, Sec-CH-DPR, DPR')], u''
