import os, sys
from wptserve.utils import isomorphic_decode
import importlib
subresource = importlib.import_module("common.security-features.subresource.subresource")

def generate_payload(server_data):
    return (u'{"headers": %(headers)s}') % server_data

def main(request, response):
    subresource.respond(request,
                        response,
                        payload_generator = generate_payload,
                        access_control_allow_origin = b"*",
                        content_type = b"application/json",
                        cache_control = b"no-store")
