# An HTTP/2 handler for testing Early Hints. Used as an entry point of Early
# Hints related tests to inject Early Hints response. See comments in
# `early-hints-helpers.sub.js`.

import json
import os
import time


def _remove_relative_resources_prefix(path):
    return path[len("resources/"):] if path.startswith("resources/") else path


def handle_headers(frame, request, response):
    preload_headers = []
    for encoded_preload in request.GET.get_list(b"preloads"):
        preload = json.loads(encoded_preload.decode("utf-8"))
        header = f'<{preload["url"]}>; rel=preload; as={preload["as_attr"]}'
        if "crossorigin_attr" in preload:
            if crossorigin := preload["crossorigin_attr"]:
                header += f"; crossorigin={crossorigin}"
            else:
                header += "; crossorigin"
        preload_headers.append(header.encode())

    # Send a 103 response.
    early_hints = [(b":status", b"103")]
    early_hints.extend((b"link", header) for header in preload_headers)
    response.writer.write_raw_header_frame(headers=early_hints,
                                           end_headers=True)

    # Simulate the response generation is taking time.
    time.sleep(0.2)
    response.status = 200
    response.headers[b"content-type"] = "text/html"
    for header in preload_headers:
        response.headers.append(b"link", header)
    response.write_status_headers()


def main(request, response):
    test_path = _remove_relative_resources_prefix(
        request.GET[b"test_url"].decode("utf-8"))
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, test_path)
    test_content = open(file_path, "r").read()
    response.writer.write_data(item=test_content, last=True)
