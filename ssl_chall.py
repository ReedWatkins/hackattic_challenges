import requests
from subprocess import run, PIPE
import store

def main():

	request = requests.get(f"https://hackattic.com/challenges/tales_of_ssl/problem?access_token={store.key}")

	j = request.json()

	priv_key = j['private_key']
	domain = j['required_data']['domain']
	serial = j['required_data']['serial_number']
	country = j['required_data']['country']
	countryCode = "".join([t[0] for t in country.split()])

	with open('priv_key.key', 'w') as f:
		f.write("-----BEGIN RSA PRIVATE KEY-----\n")
		f.write(priv_key+'\n')
		f.write("-----END RSA PRIVATE KEY-----")

	with open('openssl.sh', 'w') as f:
		f.write("#!/bin/sh"+'\n\n')
		f.write(f"openssl req -key priv_key.key -nodes -x509 -set_serial {serial} -out cert.pem")

	run(["./openssl.sh"], stdout=PIPE, 
		input = f"{countryCode}\n{country}\n\n\n\n{domain}\n\n",
		encoding = "ascii")

	run(["./convertCert.sh"])

if __name__ == '__main__':
	main()
