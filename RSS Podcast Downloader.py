import feedparser

rssFeed = "https://feeds.simplecast.com/6_oR5wn4"

feed = feedparser.parse(rssFeed)
rssEntries = feed.entries

x=0
for rows in rssEntries:
	rssLinks = rssEntries[x].links
	x+=1
	for rows in rssLinks:
		downloadLink = rssLinks[1]
		print(downloadLink['href'])



