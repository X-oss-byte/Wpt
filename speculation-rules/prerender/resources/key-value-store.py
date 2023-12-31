"""Key-Value store server.

The request takes "key=" and "value=" URL parameters. The key must be UUID
generated by token().

- When only the "key=" is specified, serves a 200 response whose body contains
  the stored value specified by the key. If the stored value doesn't exist,
  serves a 200 response with an empty body.
- When both the "key=" and "value=" are specified, stores the pair and serves
  a 200 response without body.
"""


def main(request, response):
    key = request.GET.get(b"key")
    if value := request.GET.get(b"value", None):
        request.server.stash.put(key, value)
        return (200, [], b"")

    # Get the value.
    data = request.server.stash.take(key)
    return (200, [], b"") if not data else (200, [], data)
