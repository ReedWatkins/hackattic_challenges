import requests
import asyncio
import websockets
import time
import store
from json import dumps

def send_solution_key(message):

	data = dumps({"secret": message})

	post_request = requests.post(f"https://hackattic.com/challenges/websocket_chit_chat/solve?access_token={store.key}", data=data)

	print(post_request.text)

async def ping_response(token):
	async with websockets.connect(f"wss://hackattic.com/_/ws/{token}") as socket:
		start_time = time.time()
		while True:
			message = await socket.recv()
			print(message)
			if message == 'ping!':
				temp_time = start_time
				ping_timer = time.time()
				duration = ping_timer - start_time
				time_btw_msg = str(int(round(duration*1000, -2)))
				await socket.send(time_btw_msg)
				start_time = time.time()

			if message.split()[0] == 'congratulations!':
				passphrase_index = message.find('"')
				send_solution_key(message[passphrase_index+1:len(message)-1])
				yield socket.close()

def main():

	token = requests.get(f"https://hackattic.com/challenges/websocket_chit_chat/problem?access_token={store.key}").json()['token']
	
	asyncio.get_event_loop().run_until_complete(ping_response(token=token))

if __name__ == '__main__':
	main()