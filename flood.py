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

# from my_profiles import SkuSkuScammer, SoldesCouponPCSScammer, RechargePCSScammer
from config import Config


class bcolors:
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def get_cookies(proxy, url, useragent, timeout):
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
		urlopen(req, timeout=timeout)
		return dict_from_cookiejar(cj)

	except URLError as e:
		print(bcolors.FAIL + str(e) + bcolors.ENDC)
	except HTTPError as e:
		print(bcolors.FAIL + str(e) + bcolors.ENDC)
	except Exception as e:
		print(bcolors.FAIL + str(e) + bcolors.ENDC)


def obtain_session_id(proxy, profile, useragent, timeout):
	if profile.sessid_url is None:
		return None

	cookies = get_cookies(proxy, profile.sessid_url, useragent, timeout)
	if not cookies or cookies is None:
		return None

	return cookies[profile.sessid_name]


proxy_error_score = {}
def is_bad_proxy(proxy, error):
	global proxy_error_score
	score = 0
	m = re.search('(Connection refused|403 Forbidden|Tunnel connection failed|Connection reset by peer)', error)
	if m is not None:
		score = 5
	m = re.search('(timed out)', error)
	if m is not None:
		score = 1

	if score > 0:
		proxy_error_score.setdefault(proxy, 0)
		proxy_error_score[proxy] += score
		if proxy_error_score[proxy] >= 5:
			return True

	return False

	
def single_shot(proxy, cfg):
	status = {}
	status['confirmed'] = False
	status['bad_proxy'] = False

	identity = generator.Identity()
	status['proxy'] = proxy
	cfg.profile.headers['user-agent'] = identity.useragent

	# If session ID is required, get one from cookies
	if cfg.profile.sessid_url is not None:
		sessid = obtain_session_id(proxy, profile, identity.useragent, cfg.get_timeout)
		if sessid is not None:
			status['sessid'] = sessid
			cfg.profile.headers['cookie'] = cfg.profile.sessid_name + '=' + sessid
		else:
			status['error'] = '<Failed to obtain SESSID>'
			return

	data = cfg.profile.forge_data(identity)
	status['data'] = str(data)
	status['identity'] = str(identity)

	req = Request(cfg.profile.post_url, data=urlencode(data).encode(), headers=cfg.profile.headers)
	proxy_support = ProxyHandler({'https': proxy})
	opener = build_opener(proxy_support)
	install_opener(opener)

	try:
		response = urlopen(req, timeout=cfg.post_timeout).read().decode()
		status['response'] = response

		# Check response
		m = re.search(cfg.profile.confirmation_regex, response)
		if m is not None:
			status['confirmed'] = True

	except URLError as e:
		status['error'] = 'URLError: ' + str(e)
		status['bad_proxy'] = is_bad_proxy(proxy, str(e))
	except HTTPError as e:
		status['error'] = 'HTTPError: ' + str(e)
	except Exception as e:
		status['error'] = 'Exception: ' + str(e)

	return status


def print_status(status, verbosity=0):
	entries = []
	if 'thread_attempt' in status:
		entries.append(bcolors.OKBLUE + status['thread_attempt'] + bcolors.ENDC + '\n')

	entries.append(bcolors.OKBLUE + 'Proxy: ' + status['proxy'] + bcolors.ENDC + '\n')
	if status['bad_proxy']:
		entries.append(bcolors.OKYELLOW + 'Proxy was weeded out: too many errors.' + bcolors.ENDC + '\n')

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


def flood(threadName, delays, proxies, cfg):
	iteration = 0
	while True:
		delay = delays[0]
		if len(delays)>1:
			delay = random.uniform(delays[0], delays[1])

		proxy = random.choice(proxies)
		status = single_shot(proxy, cfg)

		if status['bad_proxy']:
			proxies.remove(proxy)

		status['thread_attempt'] = threadName + ': attempt #' + str(iteration)
		print_status(status, 0)

		if 'error' not in status:
			time.sleep(delay)
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

	# Init
	generator.load_tables()
	cfg = Config()
	locator = ProxyLocator(cfg.proxy_handlers)

	# Multi-threaded fullon attack
	if mode == 'm':
		try:
			_thread.start_new_thread(flood, ('Thread-1', [.010], locator.proxies, cfg,))
			_thread.start_new_thread(flood, ('Thread-2', [.010], locator.proxies, cfg,))
			_thread.start_new_thread(flood, ('Thread-3', [.010], locator.proxies, cfg,))
			_thread.start_new_thread(flood, ('Thread-4', [.010], locator.proxies, cfg,))
		except:
			print("Error: unable to start thread")
		while 1:
			pass

	# Stealth
	elif mode == 's':
		flood('Thread-1', [10,60], locator.proxies, cfg)

	# One-shot
	elif mode == 'o':
		proxy = random.choice(locator.proxies)
		status = single_shot(proxy, cfg)
		print_status(status, verbosity)

	# Cookies analysis
	elif mode == 'c':
		proxy = random.choice(locator.proxies)
		print(bcolors.OKYELLOW + 'proxy: ' + proxy + bcolors.ENDC)
		cookies = get_cookies(proxy, url, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')
		print(cookies)


if __name__ == '__main__':
    main(sys.argv[1:])