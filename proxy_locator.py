#!/usr/bin/python3

from urllib.parse import urlencode
from urllib.request import Request, urlopen, ProxyHandler, build_opener, install_opener

import shlex  
import re
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


class ProxyHandler:
	"""
	Base class for proxy list website API handler
	"""
	def __init__(self, country, proxy_type):
		self.headers = {'accept': 'text/html',
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
		self.country = country
		self.proxy_type = proxy_type


class ProxyListDownloadHandler(ProxyHandler):
	def __init__(self, country='FR', proxy_type='https'):
		ProxyHandler.__init__(self, country, proxy_type)
		self.url = 'https://www.proxy-list.download/api/v1/get?type=' + self.proxy_type \
				 + '&country=' + self.country

	def get(self):
		req = Request(self.url, headers=self.headers)
		response = urlopen(req).read().decode()
		return response.split('\r\n')


class PubProxyHandler(ProxyHandler):
	def __init__(self, country='FR', proxy_type='https'):
		ProxyHandler.__init__(self, country, proxy_type)
		self.url = 'http://pubproxy.com/api/proxy?limit=500&format=txt&http=true&type=' + self.proxy_type \
				 + '&country=' + self.country

	def get(self):
		req = Request(self.url, headers=self.headers)
		response = urlopen(req).read().decode()
		return response.split('\n')


class ProxyLocator:
	proxies = []

	def __init__(self):
		print("Getting proxy list")

		handlers = [ProxyListDownloadHandler(country='FR'), 
					PubProxyHandler(country='FR')
					]

		# Merge responses and remove duplicate entries
		for handler in handlers:
			self.proxies = list(set(self.proxies + handler.get()))

		# Filter invalid entries
		regex = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\:[0-9]{1,5}')
		self.proxies = [p for p in self.proxies if regex.search(p)]

		print('found ' + str(len(self.proxies)) + ' proxies')

	def show_latency(self):
		for proxy in self.proxies:
			latency = get_latency(proxy)
			print('proxy: ' + proxy + ' -> ' + str(latency) + 'ms')


def main():
	locator = ProxyLocator()
	# locator.show_latency()
	print(locator.proxies)

if __name__ == '__main__':
    main()
