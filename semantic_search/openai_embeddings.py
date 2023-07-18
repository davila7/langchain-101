import streamlit as st
import os
from utils import (
    parse_docx,
    parse_pdf,
    parse_txt,
    parse_csv,
    search_docs,
    embed_docs,
    text_to_docs,
    get_sources,
)
from openai.error import OpenAIError
from dotenv import load_dotenv
import datetime

load_dotenv()

def clear_submit():
    st.session_state["submit"] = False

st.markdown('<h1>Semantic Search 🔍<small> by <a href="https://judini.ai">Judini</a></small></h1>', unsafe_allow_html=True)

# Sidebar
index = None
doc = None
with st.sidebar:
    st.session_state["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    uploaded_file = st.file_uploader(
        "Upload a pdf, docx, or txt file",
        type=["pdf", "docx", "txt", "csv"],
        help="Scanned documents are not supported yet!",
        on_change=clear_submit,
    )

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            doc = parse_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            doc = parse_docx(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            doc = parse_csv(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            doc = parse_txt(uploaded_file)
        else:
            st.error("File type not supported")
            doc = None
        text = text_to_docs(doc)
        try:
            with st.spinner("Indexing document... This may take a while⏳"):
                result = embed_docs(text)
                index = result[0]
                embeddings = result[1]
                st.session_state["api_key_configured"] = True
        except OpenAIError as e:
            st.error(e._message)

tab1, tab2 = st.tabs(["Intro", "Semantic Search"])
with tab1:
    st.markdown("### Semantic Search with cosine similarity")
    st.write("Cosine similarity is a technique used to measure the similarity between two vectors. In the context of OpenAI's embedding API, cosine similarity is used to compare the similarity between two pieces of text based on their underlying vector representations.")
    st.markdown('<img width="701" alt="Captura de Pantalla 2023-02-25 a la(s) 2 28 38 p  m" src="https://user-images.githubusercontent.com/6216945/221375969-ba8b2349-fbc4-4070-abb7-92a21ed2b265.png">', unsafe_allow_html=True)
    st.write("### Here's how it works:")
    st.write("1. First, the embedding API converts each piece of text into a vector representation using a pre-trained language model. This vector represents the meaning and context of the text.")
    st.write("2. The cosine similarity function then takes these two vectors and calculates the cosine of the angle between them. The cosine similarity score ranges from -1 to 1, where 1 indicates that the two vectors are identical, 0 indicates that they are completely dissimilar, and -1 indicates that they are exact opposites.")
    st.write("3. This cosine similarity score is then used to determine the similarity between the two pieces of text. For example, if the cosine similarity score is close to 1, the two pieces of text are likely very similar in meaning, while a score close to 0 suggests that they are completely different.")
    st.write("Overall, cosine similarity is a powerful tool for comparing the semantic similarity between two pieces of text, and OpenAI's embedding API makes it easy to implement this technique in your own projects.")
    st.markdown("""---""")
    st.markdown("## Semantic Search was written with the following tools:")
    st.markdown("#### Code GPT")
    st.write("All code was written with the help of Code GPT. Visit <a href='https://codegpt.co'>https://codegpt.co</a> to get the extension.", unsafe_allow_html=True)
    st.markdown("#### Streamlit")
    st.write("The design was written with <a href='https://streamlit.io/' target='_blank'>Streamlit</a>.", unsafe_allow_html=True)
    st.markdown("#### LangChain")
    st.markdown('<a href="https://platform.openai.com/docs/guides/embeddings">Embeddings</a> is done via the OpenAI API with "text-embedding-ada-002" and LangChain.', unsafe_allow_html=True)
    st.markdown("<a href='https://github.com/facebookresearch/faiss'>FAISS</a> Facebook AI Similarity Search is a library for efficient similarity search and clustering of dense vectors.", unsafe_allow_html=True)
    st.markdown("""---""")
    st.write('Author: <a href="https://www.linkedin.com/in/daniel-avila-arias/">Daniel Avila</a>', unsafe_allow_html=True)
    st.write('Repo: <a href="https://github.com/davila7/semantic-search">Github</a>', unsafe_allow_html=True)
    st.write("This software was developed with Code GPT, for more information visit: https://codegpt.co")
with tab2:
    st.write('To obtain an API Key you must create an OpenAI account at the following link: https://openai.com/api/')
    query = st.text_area("Ask a question about the document", on_change=clear_submit)
    button = st.button("Submit")
    if button or st.session_state.get("submit"):
        if not query:
            st.error("Please enter a question!")
        else:
            st.session_state["submit"] = True
            sources = search_docs(index, query)
            st.markdown("#### Sources")
            for source in sources:
                st.markdown(source.page_content)
                st.markdown(source.metadata["source"])
                st.markdown("---")