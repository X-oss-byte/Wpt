import time

def main(request, response):
    key = request.GET.first(b"key")

    if request.method != u"POST":
        return request.server.stash.take(key, u'/scroll-to-text-fragment/')
    # Received result data from target page
    request.server.stash.put(key, request.body, u'/scroll-to-text-fragment/')
    return u"ok"
