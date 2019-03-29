import hashlib
import hmac
import base64
from binascii import hexlify
import scrypt
import requests
from json import dumps

request = requests.get("https://hackattic.com/challenges/password_hashing/problem?access_token=b4116d855f2f8b1f")
j = request.json()
print(request.json())

password = bytes(j['password'], 'utf-8')
salt = bytes(j['salt'], 'utf-8')
decodedSalt = base64.b64decode(salt)

sha256 = hashlib.sha256(password).hexdigest()

hmac256 = hmac.new(decodedSalt, password, hashlib.sha256).hexdigest()

pbkdf2 = hexlify(hashlib.pbkdf2_hmac(j['pbkdf2']['hash'], password, decodedSalt, j['pbkdf2']['rounds'])).decode('utf-8')

'''
		Need to fix the scrypt part of this
'''
N = j['scrypt']['N']
r = j['scrypt']['r']
p = j['scrypt']['p']
buflen = j['scrypt']['buflen']
scrypt = hexlify(scrypt.hash(password, salt, N, r, p, buflen)).decode('utf-8')

print(f"Base SHA-256: {sha256}")
print(f"HMAC-256: {hmac256}")
print(f"PBKDF-SHA256: {pbkdf2}")
print(f"SCRYPT: {scrypt}")

data = dumps({'sha256': sha256,
				'hmac': hmac256,
				'pbkdf2': pbkdf2,
				'scrypt': scrypt})

post = requests.post("https://hackattic.com/challenges/password_hashing/solve?access_token=b4116d855f2f8b1f", data = data)
print(post.text)