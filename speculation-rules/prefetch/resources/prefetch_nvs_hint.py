import time

def main(request, response):
  uuid = request.GET[b"uuid"]
  prefetch = request.headers.get(
      "Sec-Purpose", b"").decode("utf-8").startswith("prefetch")
  if b"unblock" in request.GET:
    request.server.stash.put(uuid, 0)
    return ''

  if b"nvs_header" in request.GET:
    nvs_header = request.GET[b"nvs_header"]
    response.headers.set("No-Vary-Search", nvs_header)

  if prefetch:
    nvswait = None
    while nvswait is None:
      time.sleep(0.1)
      nvswait = request.server.stash.take(uuid)

  return f'<!DOCTYPE html>\n<script src="/common/dispatcher/dispatcher.js"></script>\n<script src="utils.sub.js"></script>\n<script>\n  window.requestHeaders = {{\n    purpose: "{request.headers.get("Purpose", b"").decode("utf-8")}",\n    sec_purpose: "{request.headers.get("Sec-Purpose", b"").decode("utf-8")}",\n    referer: "{request.headers.get("Referer", b"").decode("utf-8")}",\n  }};\n  const uuid = new URLSearchParams(location.search).get("uuid");\n  window.executor = new Executor(uuid);\n</script>\n'
