import requests
import store
from json import dumps
from subprocess import run, PIPE, check_output

def main():

	zip_url = requests.get(f"https://hackattic.com/challenges/brute_force_zip/problem?access_token={store.key}").json()['zip_url']

	run(['wget', '-q', '-O', 'secret.zip', zip_url])
	fcrackoutput = check_output(['./zip_crack.sh'])

	password = fcrackoutput.decode('utf-8').strip('\n').split()[-1]

	run(['unzip', '-P', password, 'secret.zip'])

	with open('secret.txt', 'r') as f:
		secret = f.read().strip('\n')

	data = dumps({"secret": secret})

	post = requests.post(f"https://hackattic.com/challenges/brute_force_zip/solve?access_token={store.key}", data = data)

	print(post.text)

if __name__ == '__main__':
	main()