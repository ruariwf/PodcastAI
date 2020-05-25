import feedparser
import requests



def episode_download(mp3_url, file_name):
	r = requests.get(mp3_url, allow_redirects=True)
	open(file_name + '.mp3', 'wb').write(r.content)


def get_mp3_download(rssFeed, limit):
	x=0
	feed = feedparser.parse(rssFeed)
	rssEntries = feed.entries
	try:
		for rows in rssEntries:
			while x < limit:
				rssLinks = rssEntries[x].links
				title = rssEntries[x].title
				x+=1
				downloadLink = rssLinks[1]
				for rows in downloadLink:
					url = downloadLink['href']
				episode_download(url, title)
				print(title + " downloaded")
	except: print("done")

get_mp3_download("https://feeds.simplecast.com/6_oR5wn4", 3)



