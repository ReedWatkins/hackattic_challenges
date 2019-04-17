import requests
import store
from json import dumps
from subprocess import run, PIPE, check_output

def main():

	request_input = requests.get(f"https://hackattic.com/challenges/collision_course/problem?access_token={store.key}").json()

	md5Coll_head = request_input['include']

	with open("input", "w") as f:
		f.write(md5Coll_head)

	#Docker container with fastcoll tool
	run(["./coll_docker.sh"])

	coll_1 = check_output(['base64', '--wrap=0', 'msg1.bin']).decode('utf-8')
	coll_2 = check_output(['base64', '--wrap=0', 'msg2.bin']).decode('utf-8')

	data = dumps({"files": [coll_1, coll_2]})

	post_request = requests.post(f"https://hackattic.com/challenges/collision_course/solve?access_token={store.key}", data=data)

	print(post_request.text)


if __name__ == '__main__':
	main()