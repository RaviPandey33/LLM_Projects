import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

import streamlit as st
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
import whisper
from pydub import AudioSegment
import os
from openai import OpenAI

# Load the Whisper model
model = whisper.load_model("base")

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key="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" )

st.title("YouTube Video Summary")

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

def transcribe_audio_with_whisper(audio_file):
    audio = AudioSegment.from_file(audio_file)
    audio.export("audio.wav", format="wav")
    result = model.transcribe("audio.wav")
    return result["text"]

def get_youtube_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en'])
        transcript = transcript.fetch()
        return ' '.join([t['text'] for t in transcript])
    except NoTranscriptFound:
        return None

def get_chatgpt_summary(transcript):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": f"Please summarize the following transcript into key points: {transcript}"}
        ]
    )
    return response.choices[0].message.content.strip()

def extract_video_id(url):
    from urllib.parse import urlparse, parse_qs
    query = urlparse(url).query
    video_id = parse_qs(query).get("v")
    if video_id:
        return video_id[0]
    else:
        return None

youtube_url = st.text_input("Enter YouTube Video URL and press Enter:")
if youtube_url:
    st.info("Processing the video...")
    video_id = extract_video_id(youtube_url)
    if video_id:
        transcript = get_youtube_transcript(video_id)
        if transcript:
            st.success("Transcript found!")
        else:
            st.warning("No transcript found. Transcribing the audio with Whisper...")
            audio_file = download_audio(youtube_url)
            transcript = transcribe_audio_with_whisper(audio_file)
            # Clean up downloaded files
            os.remove(audio_file)
            os.remove("audio.wav")
        
        st.text_area("Transcript:", transcript, height=300)
        summary = get_chatgpt_summary(transcript)
        st.text_area("ChatGPT Summary:", summary, height=300)
    else:
        st.error("Invalid YouTube URL")

