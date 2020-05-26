import feedparser
import requests
import datetime
filepath = "C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/Code/audio/"


def episode_download(mp3_url, file_name):
	illegal = ['NUL','\',''//',':','*','"','<','>','|']
	for i in illegal:
		cfile_name = file_name.replace(i, '')
	r = requests.get(mp3_url, allow_redirects=True)
	print(cfile_name)
	open(filepath + cfile_name + '.mp3', 'wb').write(r.content)


def get_mp3_download(rssFeed, limit):
	x=0
	feed = feedparser.parse(rssFeed)
	rssEntries = feed.entries
	try:
		for rows in rssEntries:
			while x < limit:
				rssLinks = rssEntries[x].links
				title = rssEntries[x].title
				publishedDate = rssEntries[x].published
				x+=1
				downloadLink = rssLinks[1]
				for rows in downloadLink:
					url = downloadLink['href']
				episode_download(url, title)
				print(title + " downloaded")
				print(publishedDate)
	except: print("done")

get_mp3_download("https://anchor.fm/s/f39a864/podcast/rss", 10)

#need to clean up names to allow the script to run
#shameless - https://rss.whooshkaa.com/rss/podcast/id/2723
#Tdts - https://feeds.simplecast.com/6_oR5wn4

