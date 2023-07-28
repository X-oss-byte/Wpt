import os


def handle_headers(frame, request, response):
    resource_url = request.GET.first(b"resource-url").decode()
    if as_value := request.GET.first(b"as", None):
        link_header_value = (
            f"<{resource_url}>; rel=modulepreload; as={as_value.decode()}"
        )
    else:
        link_header_value = f"<{resource_url}>; rel=modulepreload"
    early_hints = [
        (b":status", b"103"),
        (b"link", link_header_value),
    ]
    response.writer.write_raw_header_frame(headers=early_hints,
                                           end_headers=True)

    response.status = 200
    response.headers[b"content-type"] = "text/html"
    response.write_status_headers()


def main(request, response):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "modulepreload-in-early-hints.html")
    with open(file_path, "r") as f:
        test_content = f.read()
    response.writer.write_data(item=test_content, last=True)
