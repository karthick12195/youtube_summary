import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import pandas as pd
import google.generativeai as palm
import re

palm.configure(api_key=st.secrets["palm_api_key"])

def palm_gen_recipe(transcript):
    st.text("Captions has {} words".format(len(transcript.split(' '))))

    defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.7,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
        'max_output_tokens': 3000,
        'stop_sequences': [],
    }
    prompt = """
    You are assuming the role of transcript summarizer. Your task is to succintly summarize the transcript of a YouTube 
    video provided for general audience. Transcript: {}
    """.format(transcript)
    try:

        response = palm.generate_text(
            **defaults,
            prompt=prompt
        )
        if response.result:
            return response.result
        else:
            return 'Palm API is unable to summarize this video due to safety concerns'
    except:
        return "Not Supported"


st.title('Summarize YT videos using captions')

video_url = st.text_input('Enter the YouTube video URL to summarize...')

if video_url:
    v_id = re.findall(r"(\?v=)(.*)&?", video_url)[0][1]
    st.markdown('Watch the video [here](https://www.youtube.com/watch?v={})'.format(v_id))
    st.markdown('### Video Summary')
    try:
        transcript = YouTubeTranscriptApi.get_transcript(v_id, languages=['en', 'en-GB', 'hi', 'en-IN'])
        transcript_txt = TextFormatter().format_transcript(transcript)
        st.markdown(palm_gen_recipe(transcript_txt))
    except:
        st.markdown('No transcripts available for this video')


