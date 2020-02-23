#!/usr/bin/python3

from urllib.parse import urlencode
from urllib.request import Request, urlopen, ProxyHandler, build_opener, install_opener

import shlex  
from subprocess import Popen, PIPE, STDOUT

def get_simple_cmd_output(cmd, stderr=STDOUT):
	"""
	Execute a simple external command and get its output.
	"""
	args = shlex.split(cmd)
	return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]

def get_latency(host):
	host = host.split(':')[0]
	cmd = "fping {host} -C 3 -q".format(host=host)
	res = [float(x) for x in get_simple_cmd_output(cmd).decode('utf-8').strip().split(':')[-1].split() if x != '-']
	if len(res) > 0:
		return sum(res) / len(res)
	else:
		return 999999

class ProxyLocator:
	proxies = []

	def __init__(self):
		url = 'https://www.proxy-list.download/api/v1/get?type=https&country=FR'

		headers = {	'accept': 'text/html',
					'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
					'cache-control': 'max-age=0',
					'content-type': 'application/x-www-form-urlencoded',
					'dnt': '1',
					'sec-fetch-mode': 'navigate',
					'sec-fetch-site': 'same-origin',
					'sec-fetch-user': '?1',
					'upgrade-insecure-requests': '1',
					'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
				}

		req = Request(url, headers=headers)
		response = urlopen(req).read().decode()
		self.proxies = response.split('\r\n')

	def show_latency(self):
		for proxy in self.proxies:
			latency = get_latency(proxy)
			print('proxy: ' + proxy + ' -> ' + str(latency) + 'ms')

def main():
	locator = ProxyLocator()
	locator.show_latency()

if __name__ == '__main__':
    main()
