import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """As a professional YouTube video summarizer, Your task is to meticulously distill the transcript text into a concise summary, highlighting the key points of the video within a limit of 250 words. Kindly provide the transcript for review, and You will promptly craft an informative summary encompassing the pivotal aspects discussed in the video."""


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]

        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("Professional YouTube Transcript Conversion Service: Transforming Transcripts into Comprehensive Notes")
logo_path = "logo.png"
st.sidebar.image(logo_path, width=150)
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
