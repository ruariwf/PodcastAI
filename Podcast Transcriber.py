from pydub import AudioSegment
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import wave
from google.cloud import storage
from pydub.utils import mediainfo
import concurrent.futures
import pandas as pd



filepath = "C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/Code/audio/"     #Input audio file path
output_filepath = "C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/Code/transcripts/" #Final transcript path
bucketname = "podcast_storage_mp3" #Name of the bucket created in the step before
executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
# Import libraries

transcriptlist = []

def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[2] == 'mp3':    
        sound = AudioSegment.from_mp3("C:/Users/ruari/test.mp3")
        new_audio_file_name = audio_file_name.split('.')[2] + '.wav'
        print(new_audio_file_name)
        sound.export(new_audio_file_name, format="wav")

def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_wav(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

def mp3_framerate(audio_file_name):
    info = mediainfo(audio_file_name)
    framerate = info['sample_rate']
    return framerate

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()
    # The name of the audio file to transcribe
#frame_rate, channels = frame_rate_channel(file_name)
#if channels > 1:
#    stereo_to_mono(file_name)

def google_transcribe(audio_file_name):
    
    file_name = filepath + audio_file_name
    '''
    mp3_to_wav(file_name)

    # The name of the audio file to transcribe
    
    frame_rate, channels = frame_rate_channel(file_name)
    
    if channels > 1:
        stereo_to_mono(file_name)
    '''
    sample_rate_mp3 = mp3_framerate(file_name)
    bucket_name = bucketname
    source_file_name = filepath + audio_file_name
    destination_blob_name = audio_file_name
    print("Uploading "+ audio_file_name)
    upload_blob(bucket_name, source_file_name, destination_blob_name)
    
    gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    transcript = ''
    print(sample_rate_mp3)
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=gcs_uri)

    config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
    sample_rate_hertz=44100,
    language_code='en-US')
    # Detects speech in the audio file
    print("Transcribing " + audio_file_name)
    operation = client.long_running_recognize(config, audio)
    response = operation.result(timeout=10000)
    for result in response.results:
        transcript += result.alternatives[0].transcript
    print("deleting " + audio_file_name)
    delete_blob(bucket_name, destination_blob_name)
    #print(transcript)
    return transcript

def write_transcripts(transcript_filename,transcript):
    f= open(output_filepath + transcript_filename,"w+")
    f.write(transcript)
    f.close()
    

def run_transcribe(audio_file_name):
    transcript = google_transcribe(audio_file_name)
    transcript_filename = audio_file_name.split('.')[0] + '.txt'
    write_transcripts(transcript_filename,transcript)
    save_to_list(audio_file_name, transcript)

def save_to_list(audio_file_name , transcript):
    transcriptlist.append([audio_file_name,transcript])



if __name__ == "__main__":
    for audio_file_name in os.listdir(filepath):
        executor.submit(run_transcribe, audio_file_name)
    dfcolumns = ['Episode' , 'Transcript']
    df = pd.DataFrame(transcriptlist,columns = dfcolumns)
    df.to_csv(r'C:/Users/ruari/Google Drive (ruari@whalepodanalytics.com)/Podcast AI/PodcastTranscript.csv', index = False)
    


