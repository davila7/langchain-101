import os
import openai
from openai.embeddings_utils import get_embedding
import json
import streamlit as st
from openai.embeddings_utils import cosine_similarity
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from getpass import getpass
from ast import literal_eval
import nomic
from nomic import atlas

load_dotenv()

MODEL = "text-embedding-ada-002"
openai.api_key = os.getenv("OPENAI_API_KEY")
nomic.login(os.getenv("NUMIC_TOKEN"))

def main():
    df = pd.read_csv("word_embeddings.csv")
    st.set_page_config(page_title="Langchain Agent AI", page_icon="🤖", layout="wide")
    st.title("Try OpenAI Embeddings")
    st.write(df)

    st.write("Search similarity")
    form = st.form('Embeddings')
    question = form.text_input("Enter your question", "")
    btn = form.form_submit_button("Run")

    if btn:
        with st.spinner("Loading"):
            # df['embedding'] = df['text'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
            # df.to_csv('word_embeddings.csv')
            search_term_vector = get_embedding(question, engine="text-embedding-ada-002")
            search_term_vector = np.array(search_term_vector)
            st.write(question+" Embeddings:")
            st.write(search_term_vector)

            st.title("similarity")
             # Convert 'embedding' column to numpy arrays
            df['embedding'] = df['embedding'].apply(lambda x: np.array(literal_eval(x)))

            df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))
            
            st.write(df.sort_values("similarities", ascending=False).head(20))

if __name__ == "__main__":
    main()