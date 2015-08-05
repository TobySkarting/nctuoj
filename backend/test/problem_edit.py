import requests

x = requests.get("http://nctuoj.twbbs.org/")
print(x.text)
