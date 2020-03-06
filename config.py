from my_profiles import SkuSkuScammer, SoldesCouponPCSScammer, RechargePCSScammer
from proxy_handlers import ProxySiteHandler, ProxyListDownloadHandler, PubProxyHandler

class Config:
	def __init__(self):
		self.profile = SkuSkuScammer()
		self.proxy_handlers = [	ProxyListDownloadHandler(country='FR'), 
								PubProxyHandler(country='FR') ]
		self.get_timeout = .800
		self.post_timeout = .500