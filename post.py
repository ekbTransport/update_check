import requests

from settings import *


def post(head: str, text: str):
	"""
	Публикация во всех соцсетях
	:param head: Заголовок (в Telegram выделяется полужирным)
	:param text: Текст
	:return: None
	"""
	if TELEGRAM is not None:
		#telegram(f'*{head}*\n{text}')
		telegram(f'{head}\n{text}')
	if VK is not None:
		vk(f'{head}\n{text}')


def telegram(text: str):
	requests.get(
		'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM),
		params=dict(
			chat_id=CHANNEL,
			text=text
			#parse_mode='MarkdownV2'
		)
	)


def vk(text: str):
	pass
