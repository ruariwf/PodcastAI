from google.cloud import language_v1
from google.cloud.language_v1 import enums
import pandas as pd

df2 = pd.DataFrame({'Representative name for the entity': [], 'Entity type': [], 'Salience score': [], 'Episode Number':[],'Episode Title':[]})
df3 = pd.DataFrame({'Representative name for the entity': [], 'Entity type': [], 'Salience score': [], 'Episode Number':[],'Episode Title':[]})

def analyze_entities(text_content, globaldf):
    globaldf = pd.DataFrame({'Representative name for the entity': [], 'Entity type': [], 'Salience score': [], 'Episode Number':[],'Episode Title':[]})
    """
    Analyzing Entities in a String

    Args:
      text_content The text content to analyze
    """
    # set downloads from file and append to data frame
    client = language_v1.LanguageServiceClient()

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)
    # Loop through entitites returned from the API
    for entity in response.entities:
        entitytypetest = enums.Entity.Type(entity.type).name
        if entitytypetest == "NUMBER" or entitytypetest == "OTHER":
            nothing = 0
        else:
            globaldf = globaldf.append({'Representative name for the entity': entity.name, 'Entity type': enums.Entity.Type(entity.type).name, 'Salience score': entity.salience, 'Episode Number':epNumber,'Episode Title':epTitle}, ignore_index=True)        
    return(globaldf)
    #globaldf = globaldf.append(df)


    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    #print(u"Language of the text: {}".format(response.language))

#Import Airtable with downloads and names
#loop through analyze entities and add in downloads for that episode [Episode #, Entity, Entity Type, Salience, YT Downloads, Podcast Downloads, Total Downloads]
data = pd.read_csv("C:/Users/ruari/arationalfeartranscripts.csv", quotechar='"', engine='python') 

dfcsv = pd.DataFrame(data)

for index, row in dfcsv.iterrows():
    epNumber = row['Episode Number']
    epTitle = row['Episode Name'] 
    transcript = row['Transcription']

    #analyze_entities(epTitle, df2)
    try:
        df3 = df3.append(analyze_entities(transcript, df2))
        print(epTitle + " completed")
    except:
        print(epTitle + " error")

df3.to_csv(r'C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/A Rational Fear/TranscriptAnalysis.csv', index = False)



