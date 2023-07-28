def main(request, response):
    token = request.GET.first(b"token")
    return b"1" if request.server.stash.take(token) is not None else b"0"
