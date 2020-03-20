import random, string
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
	"""
	Website is down.
	"""
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


def fake_PCS():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


def fake_PCS_amount():
	amounts = [20, 50, 100, 150, 250]
	return random.choice(amounts)


class SoldesCouponPCSScammer(ScammerProfile):
	def __init__(self):
		ScammerProfile.__init__(self, 'https://soldes-coupon.com/index.php/verification/#wpcf7-f51-p17-o1')
		self.headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
						'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
						'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryxsDpseKLqMQ2Xj87',
						'dnt': '1',
						'origin': 'https://soldes-coupon.com',
						'referer': 'https://soldes-coupon.com/index.php/verification/',
						'sec-fetch-mode': 'cors',
						'sec-fetch-site': 'same-origin',
						'x-requested-with': 'XMLHttpRequest'
						}
		self.confirmation_regex = '(<title>VÉRIFIEZ VOTRE RECHARGE ICI &#8211; SOLDES COUPON</title>)'

	def forge_data(self, identity):
		return {'_wpcf7': '51',
				'_wpcf7_version': '5.1.4',
				'_wpcf7_locale': 'fr_FR',
				'_wpcf7_unit_tag': 'wpcf7-f51-p17-o1',
				'_wpcf7_container_post': '17',
				'email': identity.email,
				'tel': identity.phone,
				'menu-397': 'PCS',
				'code': fake_PCS(),
				'montant': fake_PCS_amount(),
				'mont': fake_PCS(),
				'montu': fake_PCS_amount(),
				'radio-125': 'OUI'
				}


class RechargePCSScammer(ScammerProfile):
	def __init__(self):
		ScammerProfile.__init__(self, 'https://rechargepcs.com/includes/action.php')
		self.sessid_url = 'https://rechargepcs.com/index.php'
		self.sessid_name = ['PHPSESSID']
		self.headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
						'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
						'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryxsDpseKLqMQ2Xj87',
						'dnt': '1',
						'origin': 'https://soldes-coupon.com',
						'referer': 'https://soldes-coupon.com/index.php/verification/',
						'sec-fetch-mode': 'cors',
						'sec-fetch-site': 'same-origin',
						'x-requested-with': 'XMLHttpRequest'
						}
		self.confirmation_regex = ''

	def forge_data(self, identity):
		return {'name': identity.surname + ' ' + identity.name,
				'email': identity.email,
				'telephone': identity.phone,
				'montant1': fake_PCS_amount(),
				'code1': fake_PCS(),
				'montant2': fake_PCS_amount(),
				'code2': fake_PCS(),
				'showcode': '0',
				'valider': 'Lancer la vérification',
				}

class LevelrunnScammer(ScammerProfile):
	def __init__(self):
		ScammerProfile.__init__(self, 'https://levelrunn.com/fr/gateway.html')
		self.sessid_url = 'https://levelrunn.com/fr/gateway.html'
		self.sessid_name = ['__cfduid','PHPSESSID_MS']
		self.headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
						'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
						'cache-control': 'max-age=0',
						'content-type': 'application/x-www-form-urlencoded',
						'dnt': '1',
						'origin': 'https://levelrunn.com',
						'referer': 'https://levelrunn.com/fr/gateway.html',
						'sec-fetch-mode': 'navigate',
						'sec-fetch-site': 'same-origin',
						'sec-fetch-user': '?1',
						'upgrade-insecure-requests': '1',
}
		self.confirmation_regex = ''

	def forge_data(self, identity):
		return {'type': 'campaign',
				'onSuccess': '/fr/approved.html',
				'onDeny': '/fr/denied.html',
				'cc-cardnumber': identity.card,
				'cc-expires-month': identity.expm,
				'cc-expires-year': identity.expy,
				'cc-cvv2': identity.cvv,
}