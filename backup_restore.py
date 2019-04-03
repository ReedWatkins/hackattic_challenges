import requests
import gzip
import base64
import store

request = requests.get(f"https://hackattic.com/challenges/backup_restore/problem?access_token={store.key}")

dump = request.json()["dump"]
dumpDecode = base64.b64decode(dump)

print(dumpDecode)

with open("db.dump", "wb") as f:
	f.write(dumpDecode)