#!/usr/bin/python3

from urllib.parse import urlencode
from urllib.request import Request, urlopen

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


class ProxyLocator:
	proxies = []

	def __init__(self, proxy_handlers):
		print("Getting proxy list")

		# Merge responses and remove duplicate entries
		for handler in proxy_handlers:
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
