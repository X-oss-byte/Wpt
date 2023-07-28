from html import escape

from wptserve.utils import isomorphic_decode

def main(request, response):
    label = request.GET.first(b'label')
    return f"""<!doctype html><meta charset="{escape(isomorphic_decode(label))}">"""
