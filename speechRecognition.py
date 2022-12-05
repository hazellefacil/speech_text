#! /usr/bin/python3
import os 
from google.cloud import speech
from scipy.io import wavfile
import noisereduce as nr
from pydub import AudioSegment 

import sys



# get json file here
__file__

service_path = os.path.join(sys.path[0], 'proj_service_key.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_path

speech_client = speech.SpeechClient()

speech_file = os.path.join(sys.path[0], 'testRecording.wav')

# load data
rate, data = wavfile.read(speech_file)

# perform noise reduction
reduced_noise = nr.reduce_noise(y=data, sr=rate)
wavfile.write(speech_file, rate, reduced_noise)

# increase volume of file
dB = 300
voice = AudioSegment.from_wav(speech_file)
louder = voice + dB
louder.export(speech_file, "wav")


# get data from the audio file
with open (speech_file, 'rb') as audio_file: 
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

# configure the wav file (you can leave the parameters blank)
config_wav = speech.RecognitionConfig(
    enable_automatic_punctuation = True,
    language_code="en-US", 
    audio_channel_count=1
)

# get the transcribed speech
response_yes = speech_client.recognize(
    config = config_wav, 
    audio = audio, 
)

f = open("transcription.txt", "w")

for result in response_yes.results:
        # The first alternative is the most likely one for this portion.
        f.write(u"{}".format(result.alternatives[0].transcript))
f.close()


