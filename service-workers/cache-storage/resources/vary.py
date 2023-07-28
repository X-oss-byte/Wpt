def main(request, response):
  if b"clear-vary-value-override-cookie" in request.GET:
    response.unset_cookie(b"vary-value-override")
    return b"vary cookie cleared"

  if set_cookie_vary := request.GET.first(b"set-vary-value-override-cookie",
                                          default=b""):
    response.set_cookie(b"vary-value-override", set_cookie_vary)
    return b"vary cookie set"

  if cookie_vary := request.cookies.get(b"vary-value-override"):
    response.headers.set(b"vary", str(cookie_vary))
  elif query_vary := request.GET.first(b"vary", default=b""):
    response.headers.set(b"vary", query_vary)

  return b"vary response"
