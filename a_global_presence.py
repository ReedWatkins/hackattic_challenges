import requests
import store
from json import dumps
from multiprocessing.pool import ThreadPool as Pool

def send_proxy_request(proxy_addr):

	proxy = proxy_addr['proxy']
	token = proxy_addr['token']

	proxy_dict = {"https": proxy}

	proxy_request = requests.get(f"https://hackattic.com/_/presence/{token}", proxies=proxy_dict)

	return proxy_request.text

def main():

	presence_token = requests.get(f"https://hackattic.com/challenges/a_global_presence/problem?access_token={store.key}").json()['presence_token']

	#No proxy needed for first request, since our own country will count as a separate code.
	non_proxy_request = requests.get(f"https://hackattic.com/_/presence/{presence_token}")
	print(non_proxy_request.text)

	proxies = [{"token": presence_token, "proxy": f"https://{x}"} for x in store.proxy_list]

	pool = Pool(6)

	for result in pool.imap(send_proxy_request, proxies):
		print(result)

	post_request = requests.post(f"https://hackattic.com/challenges/a_global_presence/solve?access_token={store.key}", data = dumps({}))

	print(post_request.text)

if __name__ == '__main__':
	main()