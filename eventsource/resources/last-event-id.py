def main(request, response):
  response.headers.set(b"Content-Type", b"text/event-stream")

  if last_event_id := request.headers.get(b"Last-Event-ID", b""):
    return b"data: " + last_event_id + b"\n\n"
  idvalue = request.GET.first(b"idvalue", u"\u2026".encode("utf-8"))
  return b"id: " + idvalue + b"\nretry: 200\ndata: hello\n\n"
