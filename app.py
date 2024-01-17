import streamlit as st
import whisper

st.title("Whisper Audio Transcriber")


@st.cache_data(show_spinner=False)
def load_whisper_model():
    model = whisper.load_model("base")
    return model


audio_file = st.file_uploader(
    "Upload an audio file", type=["wav", "mp3", "m4a"])


if audio_file is not None:
    st.subheader("Original Audio", divider="rainbow")
    st.audio(audio_file, format=audio_file.type)
    if st.button("Transcribe Audio"):
        st.success("Transcribing Audio...")
        model = load_whisper_model()
        result = model.transcribe(audio_file.name)
        st.success("Translation complete!")
        # st.write(result)
        st.write(result["text"])
else:
    st.error("Please upload an audio file!")
