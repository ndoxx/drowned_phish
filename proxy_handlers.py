from urllib.request import Request, urlopen

class ProxySiteHandler:
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


class ProxyListDownloadHandler(ProxySiteHandler):
	def __init__(self, country='FR', proxy_type='https'):
		ProxySiteHandler.__init__(self, country, proxy_type)
		self.url = 'https://www.proxy-list.download/api/v1/get?type=' + self.proxy_type \
				 + '&country=' + self.country

	def get(self):
		req = Request(self.url, headers=self.headers)
		try:
			response = urlopen(req, timeout=1).read().decode()
			return response.split('\r\n')
		except:
			return []


class PubProxyHandler(ProxySiteHandler):
	def __init__(self, country='FR', proxy_type='https'):
		ProxySiteHandler.__init__(self, country, proxy_type)
		self.url = 'http://pubproxy.com/api/proxy?limit=500&format=txt&http=true&type=' + self.proxy_type \
				 + '&country=' + self.country

	def get(self):
		req = Request(self.url, headers=self.headers)
		try:
			response = urlopen(req, timeout=1).read().decode()
			return response.split('\n')
		except:
			return []
