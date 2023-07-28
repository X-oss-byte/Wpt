def main(request, response):
    user = request.auth.username
    password = request.auth.password

    if user == b"user" and password == b"password":
        return b"Authentication done"

    realm = request.GET.first(b"realm") if b"realm" in request.GET else b"test"
    return ((401, b"Unauthorized"),
            [(b"WWW-Authenticate", b'Basic realm="' + realm + b'"')],
            b"Please login with credentials 'user' and 'password'")
