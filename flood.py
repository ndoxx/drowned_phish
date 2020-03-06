#!/usr/bin/python3

from urllib.parse import urlencode
from urllib.request import Request, urlopen, ProxyHandler, HTTPCookieProcessor, build_opener, install_opener
from urllib.error import URLError, HTTPError
from http.cookiejar import CookieJar
from requests.utils import dict_from_cookiejar
import time
import re
import _thread
import random
import sys, getopt

import generator
from proxy_locator import ProxyLocator

from my_profiles import SkuSkuScammer, SoldesCouponPCSScammer, RechargePCSScammer


class bcolors:
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def get_cookies(proxy, url, useragent):
	proxy_support = ProxyHandler({'https': proxy})
	cj = CookieJar()
	opener = build_opener(proxy_support, HTTPCookieProcessor(cj))
	install_opener(opener)

	headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			   'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
			   'cache-control': 'no-cache',
			   'dnt': '1',
			   'pragma': 'no-cache',
			   'referer': 'https://www.google.com',
			   'sec-fetch-mode': 'navigate',
			   'sec-fetch-site': 'same-origin',
			   'sec-fetch-user': '?1',
			   'upgrade-insecure-requests': '1',
			   'user-agent': useragent,
			   }

	req = Request(url, data=None, headers=headers, method='GET')
	try:
		urlopen(req, timeout=.500)
		return dict_from_cookiejar(cj)

	except URLError as e:
		print(bcolors.FAIL + str(e) + bcolors.ENDC)
	except HTTPError as e:
		print(bcolors.FAIL + str(e) + bcolors.ENDC)


def obtain_session_id(proxy, profile, useragent):
	if profile.sessid_url is None:
		return None

	cookies = get_cookies(proxy, profile.sessid_url, useragent)
	if not cookies or cookies is None:
		return None

	return cookies[profile.sessid_name]

	
def single_shot(proxies, profile):
	status = {}
	status['confirmed'] = False

	identity = generator.Identity()
	proxy = random.choice(proxies)
	status['proxy'] = proxy
	profile.headers['user-agent'] = identity.useragent

	# If session ID is required, get one from cookies
	if profile.sessid_url is not None:
		sessid = obtain_session_id(proxy, profile, identity.useragent)
		if sessid is not None:
			status['sessid'] = sessid
			profile.headers['cookie'] = profile.sessid_name + '=' + sessid
		else:
			status['error'] = '<Failed to obtain SESSID>'
			return

	data = profile.forge_data(identity)
	status['data'] = str(data)
	status['identity'] = str(identity)

	req = Request(profile.post_url, data=urlencode(data).encode(), headers=profile.headers)
	proxy_support = ProxyHandler({'https': proxy})
	opener = build_opener(proxy_support)
	install_opener(opener)

	try:
		response = urlopen(req, timeout=.500).read().decode()
		status['response'] = response

		# Check response
		m = re.search(profile.confirmation_regex, response)
		if m is not None:
			status['confirmed'] = True

	except URLError as e:
		status['error'] = str(e)
	except HTTPError as e:
		status['error'] = str(e)
	except Exception as e:
		status['error'] = e.message

	return status


def print_status(status, verbosity=0):
	entries = []
	if 'thread_attempt' in status:
		entries.append(bcolors.OKBLUE + status['thread_attempt'] + bcolors.ENDC + '\n')

	entries.append(bcolors.OKBLUE + 'Proxy: ' + status['proxy'] + bcolors.ENDC + '\n')

	if 'error' in status:
		entries.append(bcolors.FAIL + status['error'] + bcolors.ENDC + '\n')
		entries.append('--------------------------------')
		print(''.join(entries))
		return

	if 'sessid' in status:
		entries.append(bcolors.OKBLUE + 'Session ID: ' + status['sessid'] + bcolors.ENDC + '\n')

	if verbosity == 0:
		entries.append(bcolors.OKYELLOW + 'Identity:\n'  + bcolors.ENDC + status['identity'] + '\n')
	else:
		entries.append(bcolors.OKYELLOW + 'Data sent:\n' + bcolors.ENDC + status['data'] + '\n')
		entries.append(bcolors.OKYELLOW + 'Response:\n' + bcolors.ENDC + status['response'] + '\n')

	if status['confirmed']:
		entries.append(bcolors.OKGREEN + 'Success!' + bcolors.ENDC + '\n')
	else:
		entries.append(bcolors.FAIL + 'Failed!' + bcolors.ENDC + '\n')

	entries.append('--------------------------------')

	print(''.join(entries))


def flood(threadName, delays, proxies, profile):
	iteration = 0
	while True:
		delay = delays[0]
		if len(delays)>1:
			delay = random.uniform(delays[0], delays[1])

		try:
			status = single_shot(proxies, profile)
			if 'error' not in status:
				time.sleep(delay)
		except:
			continue

		status['thread_attempt'] = threadName + ': attempt #' + str(iteration)
		print_status(status, 0)
		iteration += 1


def usage():
	print('flood.py "hc:omsv"')


def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hc:omsv", ["help"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err))
		usage()
		sys.exit(2)

    # Stealth mode by default
	mode = 's'
	verbosity = 0
	url = None

	for o, a in opts:
		if o == "-v":
			verbosity = 1
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-m", "--multithreaded"):
			mode = 'm'
		elif o in ("-s", "--stealth"):
			mode = 's'
		elif o in ("-o", "--oneshot"):
			mode = 'o'
		elif o in ("-c", "--cookie"):
			mode = 'c'
			url = a
			print("Analyzing cookies from: " + url)
		else:
			assert False, "unhandled option"

	generator.load_tables()

	# Init
	locator = ProxyLocator()
	profile = SkuSkuScammer()
	# profile = SoldesCouponPCSScammer()
	# profile = RechargePCSScammer()

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
		status = single_shot(locator.proxies, profile)
		print_status(status, verbosity)
	elif mode == 'c':
		proxy = random.choice(locator.proxies)
		print(bcolors.OKYELLOW + 'proxy: ' + proxy + bcolors.ENDC)
		cookies = get_cookies(proxy, url, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')
		print(cookies)


if __name__ == '__main__':
    main(sys.argv[1:])