## This works perfectly. But this use google text to speach api and once transcript is made it then uses
## OpenAI Api to find summer of it .

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

def transcribe_audio_in_chunks(audio_file, chunk_length=60, retries=3):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file)
    transcript = ""

    for i in range(0, len(audio), chunk_length * 1000):
        chunk = audio[i:i + chunk_length * 1000]
        chunk.export("audio_chunk.wav", format="wav")
        with sr.AudioFile("audio_chunk.wav") as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_content = recognizer.record(source)
        
        chunk_transcript = ""
        for attempt in range(retries):
            try:
                chunk_transcript = recognizer.recognize_google(audio_content)
                transcript += chunk_transcript + " "
                break
            except sr.RequestError as e:
                st.warning(f"Attempt {attempt + 1}/{retries} for chunk {i // (chunk_length * 1000) + 1} failed: {e}")
                time.sleep(2)  # Wait a bit before retrying
            except sr.UnknownValueError:
                st.error(f"Google Speech Recognition could not understand chunk {i // (chunk_length * 1000) + 1}")
                break

        if not chunk_transcript:
            st.warning(f"Skipping chunk {i // (chunk_length * 1000) + 1} due to transcription issues.")
    
    return transcript

def get_chatgpt_summary(transcript):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": f"Please summarize the following transcript: {transcript}"}
        ]
    )
    return response.choices[0].message.content.strip()

youtube_url = st.text_input("Enter YouTube Video URL and press Enter:")
if youtube_url:
    st.info("Downloading and processing the video...")
    try:
        audio_file = download_audio(youtube_url)
        st.info("Transcribing the audio...")
        transcript = transcribe_audio_in_chunks(audio_file)
        if transcript:
            st.text_area("Transcript:", transcript, height=300)

            st.info("Summarizing the transcript with ChatGPT...")
            summary = get_chatgpt_summary(transcript)
            st.text_area("ChatGPT Summary:", summary, height=300)

        # Clean up downloaded files
        os.remove(audio_file)
        os.remove("audio_chunk.wav")
    except Exception as e:
        st.error(f"An error occurred: {e}")
