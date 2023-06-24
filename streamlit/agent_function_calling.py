import openai
import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv

# Setting page title and header
st.set_page_config(page_title="OpenAI Chat", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>ChatBot Streamlit OpenAI</h1>", unsafe_allow_html=True)