def main(request, response):
    time = request.url_parts.query if request.url_parts.query else u'0'
    return (
        200,
        [[b'Content-Type', b'text/html']],
        f'<meta http-equiv=refresh content={time}>',
    )
