import feedparser

rssFeed = "https://feeds.simplecast.com/6_oR5wn4"

feed = feedparser.parse(rssFeed)
print(feed.entries[0].links)
