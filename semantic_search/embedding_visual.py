import os
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import streamlit as st
import pandas as pd
import numpy as np
from ast import literal_eval
import nomic
from nomic import atlas

from dotenv import load_dotenv
load_dotenv()

MODEL = "text-embedding-ada-002"
openai.api_key = os.getenv("OPENAI_API_KEY")
nomic.login(os.getenv("NUMIC_TOKEN"))

def main():
    df = pd.read_csv("food_review.csv")
    st.set_page_config(page_title="Langchain Agent AI", page_icon="🤖", layout="wide")
    st.title("Try OpenAI Embeddings")
    st.title("Embeddings")
    st.write(df)
    st.write("Search similarity")
    form = st.form('Embeddings')
    question = form.text_input("Search similarity", "")
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
            
            # Convert to a list of lists of floats
            embeddings = np.array(df.embedding.to_list())            
            df = df.drop('embedding', axis=1)
            df = df.rename(columns={'Unnamed: 0': 'id'})

            data = df.to_dict('records')
            project = atlas.map_embeddings(embeddings=embeddings, data=data,
                                        id_field='id',
                                        colorable_fields=['Score'])
            map = project.maps[0]

            st.write(project)

            # st.write(map)



if __name__ == "__main__":
    main()