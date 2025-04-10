import pyaudio
import wave
import streamlit as st
import os
import subprocess

# Define constants for recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "./shared_data/input_audio.wav"  # Updated location for saving audio

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Function to start recording
def start_recording():
    st.session_state.frames = []  # Reset frames each time recording starts

    # Open the audio stream
    st.session_state.stream = audio.open(format=FORMAT, channels=CHANNELS,
                                         rate=RATE, input=True,
                                         frames_per_buffer=CHUNK)
    st.session_state.is_recording = True  # Set state to recording
    st.write("Recording... Press 'Stop Recording' to finish.")

    # Read audio stream in a loop and append to frames
    while st.session_state.is_recording:
        data = st.session_state.stream.read(CHUNK)
        st.session_state.frames.append(data)

# Function to stop recording and save the file
def stop_recording():
    if st.session_state.is_recording:
        # Stop the audio stream
        st.session_state.stream.stop_stream()
        st.session_state.stream.close()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(WAVE_OUTPUT_FILENAME), exist_ok=True)

        # Save the recorded audio as a .wav file in the shared_data directory
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(st.session_state.frames))

        st.write(f"Recording stopped. Audio saved to {WAVE_OUTPUT_FILENAME}.")

        # Check if the file exists before trying to play it
        if os.path.exists(WAVE_OUTPUT_FILENAME):
            st.audio(WAVE_OUTPUT_FILENAME)  # Display audio player
        else:
            st.error("Error: Audio file not found!")

        # Reset the session state for next recording
        st.session_state.is_recording = False

# Function to run a subprocess with the given command
def run_app(command):
    """
    Run a subprocess with the given command.
    Wait for it to complete.
    """
    try:
        subprocess.run(command, check=True)
        print(f"Successfully ran: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(command)}: {e}")
        raise

# Function to run the entire pipeline
def run_pipeline():
    try:
        # Step 1: Run App0 (record audio)
        # st.text("Step 1: Running audio recording...")
        # run_app(["env_trans/Scripts/python", "apps/audio_record.py"])

        # Step 2: Run App1 (transcribe and translate audio)
        st.text("Step 2: Transcribing and translating audio...")
        run_app(["env_trans/Scripts/python", "apps/audio_transcribe_translate.py"])

        # Step 3: Run App2 (process text with LLM)
        st.text("Step 3: Processing text with LLM...")
        run_app(["env_llm/Scripts/python", "apps/text_processor.py"])

        # Step 4: Run App3 (translate and generate speech)
        st.text("Step 4: Generating speech...")
        run_app(["env_trans/Scripts/python", "apps/speech_generator.py"])

        st.success("Workflow completed successfully!")
        return True  # Indicate that the pipeline was successful

    except subprocess.CalledProcessError as e:
        st.error(f"Error occurred while running the workflow: {e}")
        return False  # Indicate that there was an error in the pipeline

# Streamlit UI
st.title("Medical Query Assistance")
st.text("Step 1: Record the Audio...")
# Initialize session state variable to track recording status
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False
if "frames" not in st.session_state:
    st.session_state.frames = []

# Create buttons for start/stop recording
start_button = None
if not st.session_state.is_recording:
    start_button = st.button("Start Recording")

stop_button = st.button("Stop Recording")

# Handle button clicks
if start_button:
    start_recording()

if stop_button:
    stop_recording()

# Add a button to start the pipeline after recording
if st.button("Start Workflow"):
    workflow_completed = run_pipeline()

    # Show the result of the workflow
    output_audio_path = "shared_data/output_audio.mp3"
    if workflow_completed and os.path.exists(output_audio_path):
        st.subheader("Generated Speech Output")
        st.audio(output_audio_path, format="audio/mp3")
    else:
        st.write("No audio output file generated yet.")
