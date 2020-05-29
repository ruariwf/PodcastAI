import feedparser
import requests
import concurrent.futures
import pandas as pd
filepath = "C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/Code/audio/"
executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

def episode_download(mp3_url, file_name):
	print("Beggining download: " + file_name)
	illegal = ['NUL','\',''//',':','*','"','<','>','|',':']
	for i in illegal:
		cfile_name = file_name.replace(i, '')
	r = requests.get(mp3_url, allow_redirects=True)
	open(filepath + cfile_name + '.mp3', 'wb').write(r.content)
	return cfile_name


def get_mp3_download(rssFeed, limit, dataframe):
	x=0
	feed = feedparser.parse(rssFeed)
	rssEntries = feed.entries
	for rows in rssEntries:
		try:
			while x < limit:
				rssLinks = rssEntries[x].links
				title = rssEntries[x].title
				publishedDate = rssEntries[x].published
				x+=1
				print(rssLinks)
				downloadLink = rssLinks[1]
				for rows in downloadLink:
					url = downloadLink['href']
				#executor.submit(episode_download, (url, title))
				try:
					cfile_name = episode_download(url, title)
					print(title + " downloaded")
					#print(publishedDate)
				except:
					print(title + " error")
				updatedf = pd.DataFrame([[title, publishedDate, cfile_name, url]],columns=dfcolumns)
				dataframe = dataframe.append(updatedf,ignore_index=True)
		except:
			print("Done")
	return(dataframe)

if __name__ == '__main__':
	dfcolumns = ['Title','Date Published','File Name', 'MP3 URL']
	df = pd.DataFrame(columns=dfcolumns)
	metadata = get_mp3_download("https://www.omnycontent.com/d/playlist/820f09cf-2ace-4180-a92d-aa4c0008f5fb/0786e9ff-0519-43d3-a0cd-aa4c0176ad25/2bf97b40-59cd-424a-ba35-aa4c0176ad25/podcast.rss", 10, df)
	metadata.to_csv(r'C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/Metadata.csv', index = False)

#shameless - https://rss.whooshkaa.com/rss/podcast/id/2723
#Tdts - https://feeds.simplecast.com/6_oR5wn4
#Hamish and Andy - https://www.omnycontent.com/d/playlist/820f09cf-2ace-4180-a92d-aa4c0008f5fb/0786e9ff-0519-43d3-a0cd-aa4c0176ad25/2bf97b40-59cd-424a-ba35-aa4c0176ad25/podcast.rss

#Bring In parralell Proccesing
#combine with other scripts
#save results in Data frame and then into CSV