def main(request, response):

    # |token| should be a unique UUID request parameter for the duration of this
    # request. It will get stored in the server stash and will be used later in
    # a query request.
    # |query| should be a request parameter indicating the request would like
    # to know how many times the server has seen the request (with the
    # same token).
    token = request.GET.first(b"token", None)
    is_query = request.GET.first(b"query", None) is not None
    with request.server.stash.lock:
        value = request.server.stash.take(token)
        count = int(value) if value is not None else 0
        if not is_query:
            count += 1
        request.server.stash.put(token, count)
    headers = [(b"Count", count)] if is_query else []
    return (200, headers, b"")
