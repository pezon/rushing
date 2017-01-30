import argparse
import logging

from dateutil.parser import parse as dateparser

from rushing.parsers import transcript_parser
from rushing.util.date import daterange
from rushing.util.web import Webpage

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

START_URL_TEMPLATE = 'http://transcripts.cnn.com/TRANSCRIPTS/%Y.%m.%d.html'
START_LINKS_MATCH_URL = '*.\.html$'
START_LINKS_NOT_TEXT = 'Did Not Air'
ARTICLE_XPATH = '//table[@id=\'cnnArticleWireFrame\']'


if __name__ == '__main__':
	argparser = argparse.ArgumentParser(description='Ingest CNN Transcripts.')
	argparser.add_argument('--startdate', action='store', default=None)
	argparser.add_argument('--enddate', action='store', default=None)

	args = argparse.parse_args()
	start_date = dateparser(args.startdate or 'Today')
	end_date = dateparser(args.enddate or 'Yesterday')

	logger.info('Start URLS from {} to {}...'.format(start_date, end_date))
	dates = daterange(start_date, end_date)
	start_urls = []
	for date in dates:
		start_url = date.strftime(START_URL_TEMPLATE)
		start_urls.append(start_url)

	logger.info('Transcription URLs...')
	transcription_urls = []
	for start_url in start_urls:
		with Webpage(url) as webpage:
			urls = webpage.links(match_url=START_LINKS_MATCH_URL,
								 not_text=START_LINKS_MATCH_TEXT)
			transcript_urls.append(url for url in urls)

	logger.info('Transcriptions...')
	transcripts = []
	for transcript_url in transcript_urls:
		with Webpage(url) as webpage:
			webpage_text = webpage.text(select=ARTICLE_XPATH)
			transcript = parse_transcript(webpage_text)
			save_model(transcript)

	logger.info('FIN!')