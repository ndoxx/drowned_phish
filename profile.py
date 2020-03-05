
class ScammerProfile:
	post_url = ''
	confirmation_regex = ''
	sessid_url = None
	sessid_name = 'PHPSESSID'
	headers = {}

	def __init__(self, url):
		self.post_url = url

	def forge_data(self, identity):
		return {}