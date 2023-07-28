import random
import time

def main(request, response):
    # no-cache itself to ensure the user agent finds a new version for each update.
    headers = [
        (b'Cache-Control', b'no-cache, must-revalidate'),
        (b'Pragma', b'no-cache'),
        (b'Content-Type', b'application/javascript'),
    ]

    # Return a different script for each access.
    return headers, f'// {time.time()} {random.random()}'
