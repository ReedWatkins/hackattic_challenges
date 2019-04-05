import requests
import store
import hashlib
from math import floor
from json import dumps

def findDifficultyPrefix(difficulty: int) -> str:
	tempDiff = difficulty
	diffStr = ""

	# 1 missing lead bit -> 0111 (7), 2 missing lead bits -> 0011 (3), etc.
	lessThan4BitVals = ['7','3','1']

	if tempDiff % 4 == 0:
		diffStr+='0'*(floor(tempDiff/4))
		return diffStr
	else:
		while tempDiff != 0:
			if tempDiff < 4:
				diffStr+=lessThan4BitVals[tempDiff-1]
				tempDiff=0
			else:
				diffStr+='0'
				tempDiff-=4
		return diffStr


def main():
	request_json = requests.get(f"https://hackattic.com/challenges/mini_miner/problem?access_token={store.key}").json()

	difficulty = request_json['difficulty']
	block_data = dumps(request_json['block']['data'], separators = (',', ':'))
	diffPrefix = findDifficultyPrefix(difficulty)

	nonce = 0
	while True:
		string = f'{{"data":{block_data},"nonce":{nonce}}}'.encode('utf-8')
		str_hash = hashlib.sha256(string).hexdigest()
		if str_hash[:len(diffPrefix)] == diffPrefix:
			break
		nonce+=1

	data = dumps({"nonce": nonce})

	send_request = requests.post(f"https://hackattic.com/challenges/mini_miner/solve?access_token={store.key}", data = data)

	# Print response to see challenge was accepted
	print(send_request.text)

if __name__ == '__main__':
	main()
