from time import sleep
from lxml import html
from urllib import urljoin

from requests import Session


class Webpage(object):
	session = Session()

	remove_tags = ['script', 'style']
	whitespace_tags = ['br', 'p', 'span', 'div', 'pre', 'blockquote']

	rate_limit = 2

	def __init__(self, url):
		self.url = url
		self.status = None
		self.response = None
		self.document = None
		self.open(url)

	def __enter__(self):
		self.open()
		sleep(self.rate_limit)
		return self

	def __exit__(self, exc_type, exc_value, tb_obj):
		# HANDLE ERROR HERE
		return True

	def open(self, url):
		self.response = self.session.get(self.url)
		if self.response.ok:
			self.document = html.fromstring(self.response.text)
		return self.response.ok

	def select(self, path):
		self.document = self.document.xpath(path)[0]

	def clean(self,
			remove_tags=None,
			whitespace_tags=None):
		remove_tags = remove_tags or self.remove_tags
		whitespace_tags = whitespace_tags or self.whitespace_tags
		for tag in self.remove_tags:
			selector = '//{}'.format(tag)
			for elem in container.xpath(selector):
				elem.getparent().remove(elem)
		for tag in self.whitespace_tags:
			selector = '//{}'.format(tag)
			for elem in container.xpath(selector):
				elem.text = '\n%s\n' % (elem.text or '')

	def links(self,
			match_text=None,
			match_url=None,
			not_text=None,
			not_url=None):
		links = webpage.xpath('//a')
		for link in links:
			text, url = link.text_content(), link.get('href', '')
			absolute_url = urljoin(self.url, url)
			if not url:
				continue
			if match_url and not\
					(match(match_url, url)\
					or match(match_url, absolute_url)):
				continue
			if not match_url and\
					(match(match_url, url)\
					or match(match_url, absolute_url)):
				continue
			if match_text and not match(not_text, text):
				continue
			if not_text and match(not_text, text):
				continue
			yield absolute_url
