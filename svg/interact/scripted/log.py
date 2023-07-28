import time

def main(request, response):
    response.headers.append(b"Content-Type", b"text/javascript")
    try:
        script_id = int(request.GET.first(b"id"))
        delay = int(request.GET.first(b"sec"))
    except:
        response.set_error(400, u"Invalid parameter")

    time.sleep(delay)

    return f"log('{script_id}')"
