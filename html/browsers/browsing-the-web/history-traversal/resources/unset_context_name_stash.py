def main(request, response):
    key = request.GET.first(b"id")
    if request.method == "POST":
        value = request.GET.first(b"value")
        request.server.stash.take(key)
        request.server.stash.put(key, value)
        return b"OK"
    else:
        value = request.server.stash.take(key)
        return value if value is not None else b"NONE"
