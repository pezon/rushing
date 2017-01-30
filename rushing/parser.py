"""
Transcript parser

"""
from datetime import datetime, timedelta
from pyparsing import *

from dateutil.parser import parse as dateparse


lbrack = Literal('[')
rbrack = Literal(']')
lparen = Literal('(')
rparen = Literal(')')
comma  = Literal(',')
colon  = Literal(':')
dash   = Literal('-')
timedigits = Word(nums, max=2)

# flags
time = Combine(timedigits + colon + timedigits)('timestamp')
timestamp = lbrack + time + colon + timedigits + rbrack 
videoclip = lparen + oneOf('BEGIN END')('videoclip').setParseAction(lambda t: \
			t[0] == 'BEGIN') + oneOf(['VIDEOTAPE', 'VIDEO CLIP']) + rparen
comment = (lparen + OneOrMore(Word(alphas)) + rparen).ignore(videoclip)

# skip
skip  = Literal('Return to Transcripts main page') + restOfLine
skip |= Literal('THIS IS A RUSH TRANSCRIPT. THIS COPY MAY NOT BE IN ITS FINAL FORM AND MAY BE UPDATED.') + restOfLine

# airdate
airdate_parser = Literal('Aired') + Word(alphas)('airdate_month') +\
				 Word(nums)('airdate_day') + comma + Word(nums)('airdate_year') +\
				 dash + timedigits('airdate_hours') + Optional(colon) +\
				 timedigits('airdate_mins') + restOfLine

# name
title = oneOf('SEN. REP.').setResultsName('title')
party_abbr = oneOf('R D I').setResultsName('party')
state_abbr = Word(alphas.upper(), max=2).setResultsName('state_abbr')
party_token = lparen + party_abbr + Optional('-' + state_abbr) + rparen
words = OneOrMore(Word(alphanums + alphas8bit + '-')).setParseAction(' '.join)

# final parser
parser = Optional(timestamp) + Optional(videoclip) + Optional(comment) + \
		 Optional(title) + words('name') + Optional(party_token) + \
		 Optional(comma + words('relation')) + Optional(comment) + \
		 colon + restOfLine('speech')
parser |= Optional(timestamp) + Optional(videoclip) + Optional(comment) + \
		  restOfLine('speech')
parser.ignore(comment).ignore(skip)


def parse_airdate(line):
	months = ['January', 'February', 'March', 'April', 'May', 'June',
			  'July', 'August', 'September', 'October', 'November', 'December']
	for t, s, e in airdate_parser.scanString(line):
		tokens = t.asDict()
		airdate_month = months.index(tokens['airdate_month']) + 1
		return datetime(int(tokens['airdate_year']), airdate_month,
						int(tokens['airdate_day']), int(tokens['airdate_hours']),
						int(tokens['airdate_mins']))
	return dateparse(line.strip('Aired'))


def parse_line(line):
	for tokens, start, end in parser.scanString(line):
		return tokens.asDict()


def split_lines(lines):
	lines = lines.split('\n')
	for line in lines:
		line = line.strip()
		if not len(line):
			continue
		yield line


def parse(text, context={}):
	date = context.get('date')
	keyword = context.get('keyword')
	lines = split_lines(text)
	next(lines) # Return to Transcripts main page
	show = Show()
	show.name = next(lines)
	show.headlines = next(lines)
	show.airdate_start = parse_airdate(next(lines))
	next(lines) # THIS IS A RUSH TRANSCRIPT
	person_lookup = {}
	for line in lines:
		line = parse_line(line)
		person = Person(line, strict=False)
		if not person.name:
			try:
				person = show.transcript[-1].person
			except IndexError:
				continue
		elif person.disambiguous in person_lookup:
			person = person_lookup[person.disambiguous]
		elif person.surname in person_lookup:
			person = person_lookup[person.surname]
		else:
			person_lookup[person.disambiguous] = person
			person_lookup[person.surname] = person
			show.people.append(person)
		if 'timestamp' in line:
			try:
				hour, minute = line['timestamp'].split(':')
				hour, minute = int(hour), int(minute)
				if hour == 24:
					hour = 0
				line['timestamp'] = datetime(show.airdate_start.year, 
											 show.airdate_start.month,
											 show.airdate_start.day,
											 hour, minute)
			except ValueError:
				# some nonsense time probably. usually 5 mins pass.
				line['timestamp'] = show.transcript[-1].timestamp\
									+ timedelta(minutes=5)
		dialog = Dialog(line, strict=False)
		dialog.person = person
		if not dialog.timestamp:
			try:
				dialog.timestamp = show.transcript[-1].timestamp
			except IndexError:
				dialog.timestamp = show.airdate_start
		if dialog.videoclip:
			video_dialog = VideoDialog(dialog.to_native(), strict=False)
			if not show.transcript[-1].videoclip:
				video = Video({
					'airdate_start': dialog.timestamp,
					'description': show.transcript[-1].speech
				}, strict=False)
				show.videos.append(video)
				show.videos[-1].sequence = len(show.videos)
			show.videos[-1].airdate_end = dialog.timestamp
			if video_dialog.speech:
				show.videos[-1].transcript.append(video_dialog)
				show.videos[-1].transcript[-1].sequence = len(show.videos[-1].transcript)
				show.videos[-1].length = len(show.videos[-1].transcript)
		if dialog.speech:
			show.transcript.append(dialog)
		show.airdate_end = dialog.timestamp
	return show