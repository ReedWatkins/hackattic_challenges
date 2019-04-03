from struct import unpack
from json import dumps
import requests
import base64
import store

'''
	Order of pack needed to decode:
		signed int
		unsigned int
		short (signed)
		float
		double
		double (big endian)
'''

request = requests.get(f"https://hackattic.com/challenges/help_me_unpack/problem?access_token={store.key}")
j = request.json()
requestBytes = base64.b64decode(j['bytes'])

myint = unpack("<i", requestBytes[:4])[0]
uint = unpack("<I", requestBytes[4:8])[0]
short = unpack("<h", requestBytes[8:10])[0]
myfloat = unpack("<f", requestBytes[12:16])[0]
double = unpack("<d", requestBytes[16:24])[0]
bige_double = unpack(">d", requestBytes[24:32])[0]

data = dumps({'int': myint,
		'uint': uint,
		'short': short,
		'float': myfloat,
		'double': double,
		'big_endian_double': bige_double
})

p = requests.post(f"https://hackattic.com/challenges/help_me_unpack/solve?access_token={store.key}", data=data)

print(p.text)