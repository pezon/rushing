
	▄▄▄  ▄• ▄▌.▄▄ ·  ▄ .▄▪   ▐ ▄  ▄▄ • 
	▀▄ █·█▪██▌▐█ ▀. ██▪▐███ •█▌▐█▐█ ▀ ▪
	▐▀▀▄ █▌▐█▌▄▀▀▀█▄██▀▐█▐█·▐█▐▐▌▄█ ▀█▄
	▐█•█▌▐█▄█▌▐█▄▪▐███▌▐▀▐█▌██▐█▌▐█▄▪▐█
	.▀  ▀ ▀▀▀  ▀▀▀▀ ▀▀▀ ·▀▀▀▀▀ █▪·▀▀▀▀ 

**Rush Ing**est: *Crawl, download, and parse news TV rush transcripts!*

Broadcast and cable news networks often [publish rush transcripts](http://transcripts.cnn.com/TRANSCRIPTS/1701/29/rs.01.html) on their website. *Rushing* contains loosely-coupled utilities to allow users to parse rush transcripts. There are also light utilities to screen scrape and crawl transcript indeces.

It's left to the user to find news sources to crawl, build searchable databases, and analyze the transcripts. *Rushing* just converts it to machine-useable text! 

## Installing

	git clone https://github.com/pezon/rushing.git
	python setup.py install

## Usage

	from rushing.parser import parse_transcript
	from rushing.util.web import Webpage

	url = http://transcripts.cnn.com/TRANSCRIPTS/1701/29/rs.01.html
	body_xpath = '//table[@id=\'cnnArticleWireFrame\']'

	with Webpage(url) as webpage:
		webpage_text = webpage.text(select=body_xpath)
		transcript = parse_transcript(webpage_text)

## Notes

Currently this project is a development stub pulled out from a different project. This library is not documented and untested. There are no tests, and there are still known edge cases. It may not even install properly. 