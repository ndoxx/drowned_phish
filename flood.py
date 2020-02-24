#!/usr/bin/python3

from urllib.parse import urlencode
from urllib.request import Request, urlopen, ProxyHandler, build_opener, install_opener
import time
import re
import _thread
import random
import sys, getopt

import generator
from proxy_locator import ProxyLocator

from my_profiles import SkuSkuScammer, NaturalHerbScammer


class bcolors:
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def single_shot(proxies, profile):
	identity = generator.Identity()
	data = profile.forge_data(identity)
	profile.headers['user-agent'] = identity.useragent
	proxy = random.choice(proxies)

	req = Request(profile.post_url, data=urlencode(data).encode(), headers=profile.headers)
	proxy_support = ProxyHandler({'https': proxy})
	opener = build_opener(proxy_support)
	install_opener(opener)

	status = bcolors.OKYELLOW + 'proxy: ' + proxy + bcolors.ENDC + '\n' \
		   + str(identity) + '\n'

	try:
		response = urlopen(req, timeout=.500).read().decode()
		# print(response)

		# Check response
		m = re.search(profile.confirmation_regex, response)
		if m is not None:
			print(status + bcolors.OKGREEN + 'Success!' + bcolors.ENDC)
		else:
			print(status + bcolors.FAIL + 'Failed!' + bcolors.ENDC)
	except urllib.error.URLError as e:
		print(status + bcolors.FAIL + e.reason + bcolors.ENDC)
		

def flood(threadName, delays, proxies, profile):
	iteration = 0
	while True:
		identity = generator.Identity()
		data = profile.forge_data(identity)
		profile.headers['user-agent'] = identity.useragent
		proxy = random.choice(proxies)

		status = bcolors.OKBLUE + threadName + ': attempt #' + str(iteration) + bcolors.ENDC + '\n' \
			   + bcolors.OKYELLOW + 'proxy: ' + proxy + bcolors.ENDC + '\n' \
			   + str(identity) + '\n'

		req = Request(profile.post_url, data=urlencode(data).encode(), headers=profile.headers)
		proxy_support = ProxyHandler({'https': proxy})
		opener = build_opener(proxy_support)
		install_opener(opener)

		delay = delays[0]
		if len(delays)>1:
			delay = random.uniform(delays[0], delays[1])

		try:
			response = urlopen(req, timeout=.500).read().decode()

			# Check response
			m = re.search(profile.confirmation_regex, response)
			if m is not None:
				print(status + bcolors.OKGREEN + 'Success!' + bcolors.ENDC + '\n--------------------------------')
				iteration += 1
				time.sleep(delay)
			else:
				print(status + bcolors.FAIL + 'Failed!' + bcolors.ENDC + '\n--------------------------------')
				break
		except:
			pass


def usage():
	print('flood.py [m={s|m}][h][v]')

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "h:omsv", ["mode=","help"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err))
		usage()
		sys.exit(2)

    # Stealth mode by default
	mode = 's'
	verbose = False

	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-m", "--multithreaded"):
			mode = 'm'
		elif o in ("-s", "--stealth"):
			mode = 's'
		elif o in ("-o", "--oneshot"):
			mode = 'o'
		else:
			assert False, "unhandled option"

	generator.load_tables()

	# Init
	locator = ProxyLocator()
	profile = SkuSkuScammer()

	if mode == 'm':
		try:
			_thread.start_new_thread(flood, ('Thread-1', [.010], locator.proxies, profile,))
			_thread.start_new_thread(flood, ('Thread-2', [.010], locator.proxies, profile,))
			_thread.start_new_thread(flood, ('Thread-3', [.010], locator.proxies, profile,))
			_thread.start_new_thread(flood, ('Thread-4', [.010], locator.proxies, profile,))
		except:
			print("Error: unable to start thread")
		while 1:
			pass
	elif mode == 's':
		flood('Thread-1', [10,60], locator.proxies, profile)
	elif mode == 'o':
		single_shot(locator.proxies, profile)


if __name__ == '__main__':
    main(sys.argv[1:])