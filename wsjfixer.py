#!/usr/bin/env python

import time
import pprint
import datetime

import feedparser
import PyRSS2Gen as RSS


SOURCEFILE="/usr/local/bin/feedlist.txt"
OUTFILE = "/var/www/html/wsjdeduped.rss"
DEBUG = False


def getfeeds(fname = SOURCEFILE):
	return open(fname).readlines()



if __name__ == "__main__":

	unique_article_ids = []
	source_article_count = 0
	rss_items = []

	feedlist = getfeeds(SOURCEFILE)
	for feed in feedlist:
		items = feedparser.parse(feed)
		if DEBUG:
			print('Number of entries: %s in %s' % (len(items['entries']), items['feed']['title']))
		source_article_count += len(items['entries'])
		for entry in items['entries']:
			if entry.id in unique_article_ids:
				pass
			else:
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
