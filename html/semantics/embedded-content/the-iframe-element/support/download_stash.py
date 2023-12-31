import time

def main(request, response):
    token = request.GET[b"token"]
    response.status = 200
    response.headers.append(b"Content-Type", b"text/html")
    if b"verify-token" in request.GET:
        return u'TOKEN_SET' if request.server.stash.take(token) else u'TOKEN_NOT_SET'
    if b"finish-delay" not in request.GET:
      # <a download>
      request.server.stash.put(token, True)
      return

    # navigation to download
    response.headers.append(b"Content-Disposition", b"attachment")
    response.write_status_headers()
    finish_delay = float(request.GET[b"finish-delay"]) / 1E3
    count = 10
    single_delay = finish_delay / count
    for _ in range(count):
        time.sleep(single_delay)
        if not response.writer.write_content(b"\n"):
          return
    request.server.stash.put(token, True)
