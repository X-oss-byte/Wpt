import random, string

def id_token():
   letters = string.ascii_lowercase
   return b''.join(random.choice(letters).encode("utf-8") for _ in range(20))

def main(request, response):
   token = request.GET.first(b"token", None)
   is_query = request.GET.first(b"query", None) != None
   with request.server.stash.lock:
      value = request.server.stash.take(token)
      count = int(value) if value != None else 0
      if is_query:
         if count < 2:
           request.server.stash.put(token, count)
      else:
         count += 1
         request.server.stash.put(token, count)

   if is_query:
      headers = [(b"Count", count)]
      content = u""
   else:
      unique_id = id_token()
      headers = [(b"Content-Type", b"text/javascript"),
                 (b"Cache-Control", b"private, max-age=0, stale-while-revalidate=60"),
                 (b"Unique-Id", unique_id)]
      content = b"report('%s')" % unique_id

   return 200, headers, content
