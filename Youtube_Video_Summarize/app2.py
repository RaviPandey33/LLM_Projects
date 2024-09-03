## audio input included

from openai import OpenAI
import streamlit as st
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import threading

# Replace 'your-api-key' with your actual OpenAI API key
client = OpenAI(api_key="your-api-key")

st.title("Chat with GPT-4")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to recognize speech from audio input
def recognize_speech(audio_data):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_data) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_content = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_content)
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, the speech recognition service is unavailable."

# Streamlit form for text input
with st.form(key='chat_form', clear_on_submit=True):
    prompt = st.text_input("Enter your question:", key='input')
    submit_button = st.form_submit_button(label='Ask')

# We need to capture audio using webrtc_streamer and then process it
audio_frames = []

def audio_frame_callback(frame: av.AudioFrame):
    audio_frames.append(frame.to_ndarray().tobytes())
    return frame

webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    client_settings=ClientSettings(
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
    ),
    video_frame_callback=None,
    audio_frame_callback=audio_frame_callback,
)

if st.button("Recognize Speech"):
    if audio_frames:
        audio_data = b"".join(audio_frames)
        text_from_audio = recognize_speech(audio_data)
        st.write(f"Recognized Text: {text_from_audio}")

        # Add recognized text to messages and send to ChatGPT
        st.session_state.messages.append({"role": "user", "content": text_from_audio})
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.markdown(f"**ChatGPT:** {answer}")
    else:
        st.warning("No audio input detected.")

# Display chat history
for message in st.session_state.messages:
    role = "User" if message["role"] == "user" else "ChatGPT"
    st.markdown(f"**{role}:** {message['content']}")

# Handle form submission
if submit_button and prompt:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send the prompt to ChatGPT and get the response
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=st.session_state.messages
    )

    # Store ChatGPT response
    answer = response.choices[0].message.content.strip()
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Display Chat
