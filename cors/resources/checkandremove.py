def main(request, response):
    token = request.GET.first(b"token")
    return u"1" if request.server.stash.remove(token) is not None else u"0"
