from pytube import YouTube
import streamlit as st
import pathlib

import whisper

st.title("Whisper Audio Transcriber")


@st.cache_resource
def load_whisper_model():
    model = whisper.load_model("base")
    return model


@st.cache_resource
def download_audio(url):
    audio = YouTube(url)
    audio_title = audio.title
    audio_file = audio.streams.filter(
        only_audio=True,
        # abr='256kbps'
    ).first().download(filename=f"{audio_title}.mp4")
    return audio.title, audio_file


@st.cache_resource(show_spinner=False)
def transcribe_audio(audio_file):
    model = load_whisper_model()
    result = model.transcribe(audio_file)
    return result["text"]


if url := st.text_input("Enter a YouTube video URL"):
    # audio = YouTube(url)
    # st.subheader(audio.title)
    with st.spinner("Downloading audio..."):
        # audio_file = ""
        audio_title, audio_file = download_audio(url)
        st.subheader(audio_title)
    if audio_file:
        file_format = pathlib.Path(audio_file).suffix[1:]
        st.audio(audio_file, format=file_format)

        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing audio..."):
                response = transcribe_audio(audio_file)
                st.write(response)
