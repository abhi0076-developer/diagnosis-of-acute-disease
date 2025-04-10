from gtts import gTTS
from playsound import playsound
from googletrans import Translator
import json

shared_file_path = "shared_data/shared_data.json"

with open(shared_file_path, "r") as f:
    shared_data = json.load(f)

model_response = shared_data.get("response")

translator = Translator()
translated_response = translator.translate(model_response, src='en', dest='kn') #kn
print(translated_response.text)
text = translated_response.text

tts = gTTS(text=text, lang="kn", slow=False) #kn
tts.save("shared_data/output_audio.mp3")
print("Audio file saved")
# playsound("shared_data/output_audio.mp3")

