import speech_recognition as sr
from googletrans import Translator
import json

r = sr.Recognizer()
audio_file_path = "shared_data/input_audio.wav"
with sr.AudioFile(audio_file_path) as source:
    audio_data = r.record(source)
text = r.recognize_google(audio_data, language='kn-IN') #kn-IN for kannada & bn-IN for bengali
print(text)

translator = Translator()
translated_text = translator.translate(text, src='kn', dest='en') #kn for kannada

print(translated_text.text)

shared_file_path = "shared_data/shared_data.json"

data_to_share = {"translated_text": translated_text.text}

# Write the data to the shared JSON file
with open(shared_file_path, "w") as f:
    json.dump(data_to_share, f)

print("Data written to json file.")

