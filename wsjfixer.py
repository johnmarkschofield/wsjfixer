#!/usr/bin/env python

import time
import pprint
import datetime

import feedparser
import PyRSS2Gen as RSS


SOURCEFILE="/usr/local/bin/feedlist.txt"
OUTFILE = "/var/www/html/wsjdeduped.rss"
ID_HISTORY_FILE = "/var/www/html/idfile.txt"
DEBUG = False


def getfeeds(fname = SOURCEFILE):
	return open(fname).readlines()



if __name__ == "__main__":

	unique_article_ids = []
	source_article_count = 0
	rss_items = []
	ID_HISTORY_THISRUN = []
	try:
		ID_HISTORY_PREV = open(ID_HISTORY_FILE, 'r').readlines()
	except IOError:
		ID_HISTORY_PREV = []

	ID_HISTORY_PREV = [ x.strip() for x in ID_HISTORY_PREV ]

	feedlist = getfeeds(SOURCEFILE)
	for feed in feedlist:
		items = feedparser.parse(feed)
		if DEBUG:
			print('Number of entries: %s in %s' % (len(items['entries']), items['feed']['title']))
		source_article_count += len(items['entries'])
		for entry in items['entries']:
			# Count new IDs

			if entry.id in unique_article_ids:
				pass
			else:
				if entry.id not in ID_HISTORY_PREV:
					ID_HISTORY_THISRUN.append(entry.id.strip())
				unique_article_ids.append(entry.id)
				rss_items.append(RSS.RSSItem(
					title = entry.title,
					link = entry.link,
					description = entry.summary,
					guid = entry.id,
					pubDate = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed)),
					))

	if DEBUG:
		print('Total number of articles in input feeds: %s' % source_article_count)
		print('Number of articles in output rss feed: %s' % len(rss_items))
	output_rss = RSS.RSS2(
		title = "John Schofield's DeDuped WSJ Feed",
		link = "http://schof.org/wsjfeed",
		description = "A collection of WSJ RSS entries, but deduped.",
		lastBuildDate = datetime.datetime.now(),
		items = rss_items)

	output_rss.write_xml(open(OUTFILE, 'w'))
	if len(ID_HISTORY_THISRUN) > 0:
		print('Found %s new entries.' % len(ID_HISTORY_THISRUN))
	historyobj = open(ID_HISTORY_FILE, 'a')
	historyobj.write('\n'.join(ID_HISTORY_THISRUN))
	historyobj.write('\n')
	historyobj.close()
