#!/usr/bin/env python3

import argparse
import urllib.request
import os
import csv
import urllib.request
import re
from bs4 import BeautifulSoup, Comment
import textrazor



textrazor.api_key = open('textrazor.token', 'r').readline()

client = textrazor.TextRazor(extractors=["topics"])

def read_urls(filename):
	with open(filename) as fd:
		reader = csv.DictReader(fd)
		for row in reader:
			yield row['url']

def fetch_page(url):
	if not url.startswith('http'):
		url = 'http://{}'.format(url)
	try:
		page = urllib.request.urlopen(url)
	except Exception as ex:
		print('ERROR: {}'.format(ex))
	else:
		return page.read()

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    if re.match('\s<!--.*-->\s', str(element)):
    	return False
    return True


import unicodedata, re
all_chars = (chr(i) for i in range(0x110000))
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
reg_control_char = re.compile('[%s]' % re.escape(control_chars))

def extract_meta(html):
	data = {}
	soup = BeautifulSoup(html, 'html.parser')
	title = soup.head.title.text
	data['title'] = title
	keywords = soup.head.find('meta', attrs={'name': 'keywords'})
	data['keywords'] = (keywords or {'content': ''})['content']
	description = soup.head.find('meta', attrs={'name': 'description'})
	data['description'] = (description or {}).get('content', '')
	print(data['title'])
	print(data['description'])
	print(data['keywords'])
	elements = soup.findAll(string=lambda x:x and not isinstance(x, Comment)) # take all elements containing text, excluding Comment
	elements = filter(visible, elements) # filter out script, css, comment, raw data, ...
	elements = filter(lambda x: len(x) > 3, elements) # filter out small texts
	texts = map(lambda x: re.sub(r'(.)\1+', r'\1\1', x.string), elements) # remove duplicated characters in texts
	texts = set(texts) # remove duplicate
	texts = map(lambda x: reg_control_char.sub('', x), texts) # remove non printable chars
	texts = sorted(texts, key=lambda a: len(a), reverse=True) # sort by lenght
	data['texts'] = []
	total_length = sum([len(txt) for txt in texts])
	cumul_length = 0
	for txt in texts:
		cumul_length += len(txt)
		weight = cumul_length * 100 / total_length
		if True or weight < 60:
			data['texts'].append(txt)
		# print(round(weight, 1), repr(txt)[:220])
	data['texts'] = '. '.join(data['texts'])

	# client.set_cleanup_mode('cleanHTML')
	# client.set_cleanup_return_cleaned(True)
	# text = str(soup)

	client.set_cleanup_mode('raw')
	text = '{title}. {description}. {keywords}. {texts}'.format(**data)

	response = client.analyze(text)
	print(response.ok, response.message, response.error)
	print('LANG', response.language)
	print('RAW', response.raw_text)
	print('CLEAN', response.cleaned_text)
	print('TOPICS')
	for topic in response.topics():
		if topic.score < 0.95:
			break
		print(topic.score, topic.label) #, topic.wikipedia_link, topic.wikidata_id)
	return data

def meta_keywords(meta):
	texts = meta['texts']
	# meta['keywords'] = 

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='extract keywords from urls')
	parser.add_argument('-i', '--input', metavar='in', type=str, help='input file in CVS format', required=True)
	parser.add_argument('-o', '--output', metavar='out', type=str, help='output file in CVS format', default='<input>-keywords.cvs')
	args = parser.parse_args()
	if args.output == '<input>-keywords.cvs':
		args.output = '{}-keywords.cvs'.format(os.path.splitext(args.input)[0])
	data = {}
	for url in read_urls(args.input):
		if url.startswith('#'):
			continue
		print('fetching url {}'.format(url))
		html = fetch_page(url)
		if html == None:
			continue
		meta_raw = extract_meta(html)
		meta = meta_keywords(meta_raw)
		print(meta)
