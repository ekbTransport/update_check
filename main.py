# -*- coding: utf-8 -*-

from urllib.parse import urljoin
from lxml import html
import requests
import json
import sys
import os

from post import post

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
if sys.platform == 'win32':
	BASE_DIR += '\\'
else:
	BASE_DIR += '/'

if __name__ == '__main__':
	try:
		with open(BASE_DIR + 'sites.json', 'r') as file:
			sites = json.load(file)
	except FileNotFoundError:
		print('А где sites.json?')

	try:
		with open(BASE_DIR + 'links.json', 'r') as file:
			old_links = json.load(file)
	except FileNotFoundError:
		with open(BASE_DIR + 'links.json', 'w') as file:
			json.dump({}, file, indent=4)
		old_links = dict()

	links = dict(old_links)

	for site in sites:
		try:
			page = requests.get(sites[site]['page'])
			if page.status_code == 200:
				tree = html.fromstring(page.content)
				links[site] = list()
				for link in tree.xpath('//a'):
					try:
						links[site].append(urljoin(sites[site]['page'], link.attrib['href']))
					except KeyError:
						pass
				links[site] = list(set(links[site]))
		except requests.exceptions.ConnectionError:
			print(f'** Не удалось подключиться к {site} **')

	push = list()
	for site in sites:
		try:
			if old_links[site] != [] and links[site] != []:
				for link in links[site]:
					if link not in old_links[site]:
						post(sites[site]['name'], link)
		except KeyError:
			pass

	with open('links.json', 'w', encoding='utf-8') as file:
		json.dump(links, file, indent=4)
