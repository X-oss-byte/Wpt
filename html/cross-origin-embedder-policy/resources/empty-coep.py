def main(request, response):
    headers = [(b'Content-Type', b'text/html')]

    headers.extend(
        (b'Cross-Origin-Embedder-Policy', value)
        for value in request.GET.get_list(b'value')
    )
    return (200, headers, u'')
