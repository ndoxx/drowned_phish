
class ScammerProfile:
	post_url = ''
	confirmation_regex = ''
	headers = {}

	def __init__(self, url):
		self.post_url = url

	def forge_data(self, identity):
		return {}