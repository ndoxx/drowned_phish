#!/usr/bin/python3

import random
import csv
import math
import codecs
import unicodedata
import re
import zipfile
from io import TextIOWrapper

import card_generator

def load_txt(path, encoding='utf-8'):
	items = []
	with open(path, 'r', encoding=encoding) as f:
		for line in f:
			items.append(line.rstrip())
	return items

def load_zipped_txt(root, path, encoding='utf-8'):
	items = []
	with root.open(path, 'r') as f:
		for line in codecs.iterdecode(f, encoding):
			items.append(line.rstrip())
	return items


def load_tables():
	global names
	global surnames
	global pseudonyms
	global emaildoms
	global addresses
	global banks
	global useragents
	global cities
	global postals
	global prefixes

	cities = []
	postals = []

	# Load data from zip file
	try:
		root = zipfile.ZipFile("data/data.zip", "r")
		names      = load_zipped_txt(root, 'names.txt')
		surnames   = load_zipped_txt(root, 'surnames.txt')
		pseudonyms = load_zipped_txt(root, 'pseudonyms.txt', encoding='latin-1')
		emaildoms  = load_zipped_txt(root, 'emaildomain.txt')
		addresses  = load_zipped_txt(root, 'addresses.txt')
		banks      = load_zipped_txt(root, 'banks.txt')
		useragents = load_zipped_txt(root, 'useragents.txt')

		with root.open('cities.csv', 'r') as f_cities:
		    csv_reader = csv.reader(TextIOWrapper(f_cities, 'utf-8'), delimiter=';')
		    for lines in csv_reader:
		    	cities.append(lines[1])
		    	postals.append(lines[2])

		with root.open('phone_prefix.csv', 'r') as f_prefixes:
			csv_reader = csv.reader(TextIOWrapper(f_prefixes, 'utf-8'), delimiter=';')
			prefixes = {rows[0]:rows[1] for rows in csv_reader}

	except Exception as e:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(e).__name__, e.args)
		print (message)

	# names      = load_txt('data/names.txt')
	# surnames   = load_txt('data/surnames.txt')
	# pseudonyms = load_txt('data/pseudonyms.txt', encoding='latin-1')
	# emaildoms  = load_txt('data/emaildomain.txt')
	# addresses  = load_txt('data/addresses.txt')
	# banks      = load_txt('data/banks.txt')
	# useragents = load_txt('data/useragents.txt')

	# with open("data/cities.csv", "r") as f_cities:
	#     csv_reader = csv.reader(f_cities, delimiter=';')
	#     for lines in csv_reader:
	#     	cities.append(lines[1])
	#     	postals.append(lines[2])

	# with open('data/phone_prefix.csv', mode='r') as f_prefixes:
	# 	reader = csv.reader(f_prefixes, delimiter=';')
	# 	prefixes = {rows[0]:rows[1] for rows in reader}


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', str(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


class Identity:
	def generate_email(self):
		"""
			Generate a real looking email address, using a name, surname,
			possibly a pseudonym and random numbers.
			Mail domains are choosen at random from a list of valid providers.
		"""
		emaildom = random.choice(emaildoms)

		if random.randint(1,10) > 3:
			mail_name     = self.name.lower()
			mail_surname  = self.surname.lower()

			mail_name     = re.sub('[\\W_-]+', '', mail_name)
			mail_surname  = re.sub('[\\W_-]+', '', mail_surname)

			if random.randint(1,10) > 6 or len(mail_surname) > 10:
				max_len   = min(random.randint(1,5), len(mail_name)-1)
				mail_name = mail_name[0:max_len]

			numbers = ''
			if random.randint(1,10) > 5 and len(mail_surname) < 10:
				if random.randint(1,10) > 4:
					numbers = self.year[2:4]
				else:
					numbers = '{:d}'.format(random.randint(1,999))

			separator = '.'
			if random.randint(1,10) > 5:
				separator = '_'
			elif random.randint(1,10) > 5:
				separator = '-'

			if random.randint(1,10) > 5:
				self.email = mail_name + separator + mail_surname + numbers + '@' + emaildom
			else:
				self.email = mail_surname + separator + mail_name + numbers + '@' + emaildom

		else:
			self.email = self.pseudo + '@' + emaildom

		self.email = remove_accents(self.email).replace(' ', '')


	def generate_phone(self):
		"""
			Generate a (French) cellphone or land-line number. Land-line numbers
			are coherent with the fake person's postal code.
		"""
		global prefixes
		key = self.postal[0:2]
		if key in prefixes and random.randint(1,10)>4:
			# Try to generate phone prefix according to postal code
			digits = str(random_with_N_digits(6))
			prefix = prefixes[key]
		else:
			# Cellphone
			digits = str(random_with_N_digits(8))
			prefix = '06'
			if(random.randint(1,10)>6):
				prefix = '07'

		self.phone = prefix + digits


	def generate_card_holder(self):
		"""
			Generate a credit card holder string. Surname can appear before or
			after name, and can be capitalized with accents removed.
		"""
		if(random.randint(1,10)>7):
			holder_surname = self.surname
		else:
			holder_surname = remove_accents(self.surname).upper()

		if(random.randint(1,10)>5):
			self.holder = self.name + ' ' + holder_surname
		else:
			self.holder = holder_surname + ' ' + self.name


	def __init__(self):
		global names
		global surnames
		global pseudonyms
		global emaildoms
		global addresses
		global cities
		global postals
		global banks
		self.name     = random.choice(names).title()
		self.surname  = random.choice(surnames).title()
		self.pseudo   = random.choice(pseudonyms).lower()
		self.username = self.name + ' ' + self.surname

		self.address  = random.choice(addresses).title()
		rnd_city_idx  = random.randint(0,len(cities)-1);
		self.city     = cities[rnd_city_idx].title()
		self.postal   = postals[rnd_city_idx]

		self.day      = '{:02d}'.format(random.randint(1,29))
		self.month    = '{:02d}'.format(random.randint(1,12))
		self.year     = str(random.randint(1940,1996))

		self.generate_email()
		self.generate_phone()

		rnd = random.Random()
		if(random.randint(1,10)>5):
			self.card = str(card_generator.generate_card("mastercard"))
		elif(random.randint(1,10)>5):
			self.card = str(card_generator.generate_card("americanexpress"))
		else:
			self.card = str(card_generator.generate_card("visa16"))

		self.expm = "{:02d}".format(random.randint(1,12))
		self.expy = str(random.randint(2019,2025))
		self.cvv  = "{:03d}".format(random.randint(0,999))
		self.bank = random.choice(banks)
		self.generate_card_holder()

		# Internet identity
		global useragents
		self.useragent = random.choice(useragents)


	def __str__(self):
		return '[' + self.username + ']\n' \
			 + 'birth: ' + self.month + '/' + self.day + '/' + self.year + '\n' \
		     + 'mail: ' + self.email + '\n' \
		     + 'address: ' + self.address + ', ' + self.postal + ' ' + self.city + '\n' \
		     + 'phone: ' + self.phone + '\n' \
		     + 'cc: ' + self.card + ' exp: ' + self.expm + '/' + self.expy + ' cvv: ' + self.cvv + ' holder: ' + self.holder + '\n' \
		     + 'bank: ' + self.bank + '\n' \
		     + 'user-agent: ' + self.useragent


def main():
	load_tables()
	random.Random().seed()
	identity = Identity()
	print(identity)


if __name__ == '__main__':
    main()
