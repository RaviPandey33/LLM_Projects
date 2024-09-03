

import streamlit as st
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import speech_recognition as sr
from openai import OpenAI
import os
import time

# Replace 'your-api-key' with your actual OpenAI API key
client = OpenAI(api_key="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")

st.title("YouTube Video Transcript with ChatGPT")

def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'noplaylist': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.download([youtube_url])
        return audio_file

def transcribe_audio(audio_file, retries=3):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file)
    audio.export("audio.wav", format="wav")
    with sr.AudioFile("audio.wav") as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_content = recognizer.record(source)
    
    for attempt in range(retries):
        try:
            transcript = recognizer.recognize_google(audio_content)
            return transcript
        except sr.RequestError as e:
            st.warning(f"Attempt {attempt + 1}/{retries} failed: {e}")
            time.sleep(2)  # Wait a bit before retrying
        except sr.UnknownValueError:
            st.error("Google Speech Recognition could not understand the audio")
            return ""
    
    st.error("All transcription attempts failed.")
    return ""

youtube_url = st.text_input("Enter YouTube Video URL and press Enter:")
if youtube_url:
    st.info("Downloading and processing the video...")
    try:
        audio_file = download_audio(youtube_url)
        st.info("Transcribing the audio...")
        transcript = transcribe_audio(audio_file)
        if transcript:
            st.text_area("Transcript:", transcript, height=300)

        # Clean up downloaded files
        os.remove(audio_file)
        os.remove("audio.wav")
    except Exception as e:
        st.error(f"An error occurred: {e}")
