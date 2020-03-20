from my_profiles import SkuSkuScammer, SoldesCouponPCSScammer, RechargePCSScammer, LevelrunnScammer
from proxy_handlers import ProxySiteHandler, ProxyListDownloadHandler, PubProxyHandler

class Config:
	def __init__(self):
		self.profile = SkuSkuScammer()
		# self.profile = LevelrunnScammer() # WIP
		# self.profile = RechargePCSScammer()
		self.proxy_handlers = [	ProxyListDownloadHandler(country='FR'),
								# ProxyListDownloadHandler(country='US'), 
								# ProxyListDownloadHandler(country='DE'), 
								# ProxyListDownloadHandler(country='GB'), 
								PubProxyHandler(country='FR'),
								PubProxyHandler(country='US'),
								PubProxyHandler(country='DE'),
								PubProxyHandler(country='GB'),]
		self.get_timeout = .800
		self.post_timeout = .500