# Diagnosis-of-Acute-Disease
Supply of doctors is limited in India especially in smaller towns and villages making provision of healthcare difficult to a large number of people. Telemedicine and other solutions in the past have also struggled to scale up due to this problem. Now in the age of digital assistants like Google and Alexa, we are using AI to tackle this problem. We have come up with a project which takes audio of the user in their desired language and provides LLM generated response for the user query. The LLM gets the medical context from documents stored which improves the accuracy of the information provided by the LLM.

## Overview
This project is a multistage Python application designed for:
1. Recording audio input.
2. Transcribing and translating the audio.
3. Processing text data using a language model.
4. Generating speech output in a target language.

It uses multiple virtual environments to manage dependencies for different stages of the pipeline.

---

## Project Workflow
The application is divided into four main stages:

1. **Audio Recording**
   - Records audio using `pyaudio`.
   - Saves the recorded audio as a `.wav` file.

2. **Transcription and Translation**
   - Transcribes the audio using Google Speech Recognition.
   - Translates the transcribed text into English (or another target language).

3. **Language Model Processing**
   - Processes the translated text using a large language model (LLM).
   - Outputs a response based on the input query.

4. **Text-to-Speech (TTS)**
   - Converts the processed text back into speech using Google Text-to-Speech (gTTS).
   - Outputs the speech in a target language.

---

## Project Structure

The recommended structure for the project files and directories is as follows:

```
project_root/
├── datasets/                             # Directory for input PDF files for LLM processing
    ├──common_diseases.pdf                # Context for the medical assistance
├── env_trans/                            # Virtual environment for transcription, translation, and TTS
├── env_llm/                              # Virtual environment for LLM processing
├── shared_data                           # Stores shared files between the applications
├── requirements                          # Stores requirements for two environments
    ├── requirements_trans.txt            # Dependencies for env_trans
    ├── requirements_llm.txt              # Dependencies for env_llm
├── apps
    ├── audio_record.py                   # Script for recording audio
    ├── audio_transcribe_translate.py     # Script for transcription and translation
    ├── text_processor.py                 # Script for processing text with the LLM
    ├── speech_generator.py               # Script for generating and playing speech output
└── run_pipeline.py                       # Main script orchestrating the workflow
```

---

## Prerequisites

1. Python 3.8 or later installed.
2. Install and activate two separate virtual environments:
   - `env_trans`: For transcription, translation, and TTS.
   - `env_llm`: For language model processing.

3. Required dependencies:
   - **env_trans:**
     - `pyaudio`
     - `wave`
     - `googletrans`
     - `gtts`
     - `playsound`
     - `speechrecognition`
   - **env_llm:**
     - `chromadb`
     - `langchain`
     - `langchain_community`
     - `sentence-transformers`
     - `openai`

---

## File Descriptions

### Main Script
**`run_pipeline.py`**
- Orchestrates the workflow by sequentially executing the submodules.
- Each stage is run using its respective virtual environment.

### Submodules
1. **Audio Recording**
   - **File:** `audio_record.py`
   - Captures audio input and saves it as `input_audio.wav`.

2. **Transcription and Translation**
   - **File:** `audio_transcribe_translate.py`
   - Transcribes the recorded audio and translates it to English.
   - Saves the translated text in a shared JSON file (`shared_data.json`).

3. **Language Model Processing**
   - **File:** `text_processor.py`
   - Processes the translated text using an LLM to generate a response.
   - Outputs the response to `shared_data.json`.

4. **Text-to-Speech**
   - **File:** `speech_generator.py`
   - Translates the LLM response into the desired target language.
   - Converts the response into speech and saves it as `output_audio.mp3`.
   - Plays the generated audio.

---

## Installation and Setup

1. Clone the repository.
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Set up virtual environments:
   ```bash
   python -m venv env_trans
   python -m venv env_llm
   ```

3. Activate environments and install dependencies:
   - For `env_trans`:
     ```bash
     source env_trans/bin/activate  # Linux/Mac
     env_trans\Scripts\activate   # Windows
     pip install -r requirements_trans.txt
     ```
   - For `env_llm`:
     ```bash
     source env_llm/bin/activate  # Linux/Mac
     env_llm\Scripts\activate   # Windows
     pip install -r requirements_llm.txt
     ```

4. Place your dataset (PDF files) in the `datasets/` directory for the LLM processing.

---

## Usage

1. Run the main script:
   ```bash
   python run_pipeline.py
   ```

2. Follow on-screen prompts for audio recording.

3. The output speech will be saved as `output_audio.mp3` and played automatically.

---

## Configuration

### File Renaming
You can rename the files for better clarity as follows:

| Current Name                | Suggested Name              |
|-----------------------------|-----------------------------|
| `app.py`                   | `run_pipeline.py`          |
| `transcribe_translate.py`   | `audio_transcribe_translate.py` |
| `llm_processor.py`          | `text_processor.py`        |
| `text_to_speech.py`         | `speech_generator.py`      |

---

## Notes

- Ensure that all virtual environments are properly activated before running the corresponding scripts.
- If using different languages, update the language codes in the scripts where required (e.g., `hi-IN` for Hindi, `kn-IN` for Kannada).

---

## License
This project is licensed under the MIT License.


