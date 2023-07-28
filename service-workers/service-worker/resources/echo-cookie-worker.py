def main(request, response):
    headers = [(b"Content-Type", b"text/javascript")]

    values = []
    for key in request.cookies:
        values.extend(
            b'"%s": "%s"' % (key, cookie.value)
            for cookie in request.cookies.get_list(key)
        )
    # Update the counter to change the script body for every request to trigger
    # update of the service worker.
    key = request.GET[b'key']
    counter = request.server.stash.take(key)
    if counter is None:
        counter = 0
    counter += 1
    request.server.stash.put(key, counter)

    body = b"""
// %d
self.addEventListener('message', e => {
  e.source.postMessage({%s})
});""" % (counter, b','.join(values))

    return headers, body
