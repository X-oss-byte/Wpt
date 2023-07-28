def main(request, response):
    # Set mode to 'init' for initial fetch.
    mode = b'init'
    if b'update-recovery-mode' in request.cookies:
        mode = request.cookies[b'update-recovery-mode'].value

    extra_body = b''

    if mode == b'bad':
        # When the update tries to pull the script again, update to
        # a worker service worker that does not break document
        # navigation.  Serve the same script from then on.
        response.delete_cookie(b'update-recovery-mode')

    elif mode == b'init':
        # Install a bad service worker that will break the controlled
        # document navigation.
        response.set_cookie(b'update-recovery-mode', b'bad')
        extra_body = b"addEventListener('fetch', function(e) { e.respondWith(Promise.reject()); });"
    headers = [
        (b'Cache-Control', b'no-cache, must-revalidate'),
        (b'Pragma', b'no-cache'),
        (b'Content-Type', b'application/javascript'),
    ]
    return headers, b'%s' % (extra_body)
