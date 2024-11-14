from urllib import parse
from urllib.parse import urlparse

url = "https://software-engineering.masterschool.com/production-pages/the-big-crash-classwork-2"
parsed_url = urlparse(url)
print(parsed_url)