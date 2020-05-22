import pandas as pd
from google.cloud import language_v1
from google.cloud.language_v1 import enums
blankDF = {'Positive Sentiment': [], 'Neutral Sentiment': [], 'Negative Sentiment': [],'Episode Sentiment Score': [],'Episode Magnitude Score': [], 'Episode Number':[],'Episode Title':[],'Avg Sentiment':[],'Percent Positive':[],'Percent Negative':[],'Percent Neutral':[],'Date Published':[]}
holderdf = pd.DataFrame(blankDF)
summarydf = pd.DataFrame(blankDF) 
def analyze_sentiment(text_content):
    sentimentdf = pd.DataFrame(blankDF) 
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    #text_content = open("C:/Users/ruari/Documents/TDTS/AI Podcast Transcripts/612 - Transcript.txt", "r")

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    # Get overall sentiment of the input document
    # Get sentiment for all sentences in the document
    positiveCount = 0
    negativeCount = 0
    neutralCount = 0
    counter = 0
    sentimentsum = 0
    for sentence in response.sentences:
        counter += 1
        sentimentsum = sentimentsum + sentence.sentiment.score
        if sentence.sentiment.score > 0:
            positiveCount +=1
        elif sentence.sentiment.score < 0:
            negativeCount += 1
        elif sentence.sentiment.score == 0:
            neutralCount += 1
    avgSentiment =sentimentsum / counter
    percentPositive = positiveCount/(positiveCount+negativeCount+neutralCount)
    percentNegative = negativeCount/(positiveCount+negativeCount+neutralCount)
    percentNeutral = neutralCount/(positiveCount+negativeCount+neutralCount)
    print(avgSentiment)
    sentimentdf = sentimentdf.append({'Positive Sentiment': positiveCount, 'Neutral Sentiment': neutralCount, 'Negative Sentiment': negativeCount,'Episode Sentiment Score': response.document_sentiment.score ,'Episode Magnitude Score': response.document_sentiment.magnitude, 'Episode Number':epNumber,'Episode Title':epTitle ,'Avg Sentiment': avgSentiment ,'Percent Positive':percentPositive,'Percent Negative':percentNegative,'Percent Neutral':percentNeutral,'Date Published':publishDate}, ignore_index=True) 
    return(sentimentdf)


data = pd.read_csv("C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/Seize The Yay/Transcript.csv", quotechar='"', engine='python')#, engine='python' 

dfcsv = pd.DataFrame(data)
print(dfcsv.head)
for index, row in dfcsv.iterrows():
    epNumber = row['Episode Number']
    epTitle = row['Episode Name'] 
    transcript = row['Transcription']
    publishDate = row['Date Published']
    #analyze_entities(epTitle, df2)
    try:
        summarydf = summarydf.append(analyze_sentiment(transcript))
        print(epTitle + " completed")
    except:
        print(epTitle + " error")
summarydf.to_csv(r'C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/Seize The Yay/Sentiment_Analysis.csv', index = False)

#C:\Users\ruari\Google Drive (ruari@whalepodanalytics.com)\Podcast AI\A Rational Fear

#C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/TDTS/Podcast Title AI/Sentiment_Analysis.csv