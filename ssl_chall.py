import requests
import key

request = requests.get(f"https://hackattic.com/challenges/tales_of_ssl/problem?access_token={key.key}")

j = request.json()

priv_key = j['private_key']
domain = j['required_data']['domain']
serial = j['required_data']['serial_number']
country = j['required_data']['country']

print(priv_key)
print(domain)
print(serial)
print(country)

with open('priv_key.key', 'w') as f:
	f.write("-----BEGIN RSA PRIVATE KEY-----\n")
	f.write(priv_key+'\n')
	f.write("-----END RSA PRIVATE KEY-----")

with open('openssl.sh', 'w') as f:
	f.write("#!/bin/bash"+'\n\n')
	f.write(f"openssl req -key priv_key.key -nodes -x509 -set_serial {serial} -out cert.pem")