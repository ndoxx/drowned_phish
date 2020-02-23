from profile import ScammerProfile

class SkuSkuScammer(ScammerProfile):
	def __init__(self):
		ScammerProfile.__init__(self, 'https://aquitementfr.tv/fr/skusku992.php')
		self.headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
						'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
						'cache-control': 'max-age=0',
						'content-type': 'application/x-www-form-urlencoded',
						'dnt': '1',
						'origin': 'https://aquitementfr.tv',
						'referer': 'https://aquitementfr.tv/fr/remboursement.php',
						'sec-fetch-mode': 'navigate',
						'sec-fetch-site': 'same-origin',
						'sec-fetch-user': '?1',
						'upgrade-insecure-requests': '1',
						'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
						}
		self.confirmation_regex = '(Demande de remboursement envoyée)'

	def forge_data(self, identity):
		return {'emaile': identity.email,
				'username': identity.username,
				'day': identity.day,
				'month': identity.month,
				'year': identity.year,
				'address': identity.address,
				'cp': identity.postal,
				'city': identity.city,
				'phone': identity.phone,
				'titu': identity.holder,
				'cc': identity.card,
				'expm': identity.expm,
				'expy': identity.expy,
				'cvc': identity.cvv
				}


class ImpotsGouvRuScammer(ScammerProfile):
	bank_abbrev = {"American Express": "amex",
				   "Axa Banque": "axa",
				   "Banque populaire": "bp",
				   "BNP": "bnp",
				   "ING": "ING",
				   "Orange Bank": "Orange Bank",
				   "Nickel": "bnp",
				   "N26": "N26",
				   "BforBank": "BforBank",
				   "Monabanq": "Monabanq",
				   "Fortuneo": "Fortuneo",
				   "Boursorama": "Boursorma",
				   "Hello bank!": "Hello bank!",
				   "Caixa": "Caixa",
				   "Banque BCP": "Banque BCP",
				   "Bred": "bred",
				   "Caisse d'épargne": "caisse",
				   "Crédit agricole": "ca",
				   "Crédit mutuel": "cm",
				   "Crédit du nord": "cn",
				   "CIC": "cic",
				   "HSBC": "hsbc",
				   "Société générale": "sg",
				   "La banque postale": "pst",
				   "LCL": "lcl",
				   "Autres": "na"
					}

	def __init__(self):
		ScammerProfile.__init__(self, 'http://impots.gouv.fr-remboursement.service.email.secure.u6179835bp.ha004.t.justns.ru/impots-gouv/impots-gouv/2020/contact/fr/gouv/fr/email/post.php')
		self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
						'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
						'Cache-Control': 'max-age=0',
						'Connection': 'keep-alive',
						'Content-Type': 'application/x-www-form-urlencoded',
						'DNT': '1',
						'Host': 'impots.gouv.fr-remboursement.service.email.secure.u6179835bp.ha004.t.justns.ru',
						'Origin': 'http://impots.gouv.fr-remboursement.service.email.secure.u6179835bp.ha004.t.justns.ru',
						'Referer': 'http://impots.gouv.fr-remboursement.service.email.secure.u6179835bp.ha004.t.justns.ru/impots-gouv/impots-gouv/2020/contact/fr/gouv/fr/email/',
						'Upgrade-Insecure-Requests': '1',
						'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
						}
		self.confirmation_regex = '(Veuillez patienter pendant que nous traitons votre demande)'

	def forge_data(self, identity):
		return {'spi': '',
				'teledec': '',
				'rfr': '',
				'AK01': identity.name,
				'AK02': identity.surname,
				'AK03': identity.day,
				'AK04': identity.month,
				'AK05': identity.year,
				'AK070': identity.address,
				'AK07': identity.postal,
				'AK06': identity.phone,
				'spi': '',
				'teledec': '',
				'rfr': '',
				'bank': self.bank_abbrev[identity.bank],
				'ccnum': identity.card,
				'expMonth': identity.expm,
				'expYear': identity.expy,
				'cvv': identity.cvv,
				'account': '',
				'ibad': '',
				'plus': '',
				'question': 'Dans quelle rue avez-vous grandi ?',
				'reponses': '',
				'question2': '',
				'reponses2': '',
				'ghazcisse': '',
				'ghazcisse0': ''
				}