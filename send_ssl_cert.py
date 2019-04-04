import requests
import store
from json import dumps

with open("b64cert", "r") as f:
	cert = f.read()

data = dumps({"certificate": cert})

request = requests.post(f"https://hackattic.com/challenges/tales_of_ssl/solve?access_token={store.key}", data = data)

print(request.text)