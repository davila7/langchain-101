import streamlit as st
import time
import requests
import json
import os
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="centered")  

col1, col2 = st.columns([2,3])

with col1:
    image = Image.open('danigpt.png')
    st.image(image, width=200)

with col2:
    st.title("DaniGPT 🤖")
st.write("Preguntame cualquier cosa sobre python, Judini o Langchain")
st.write("OJO 👀 No estoy conectado a internet, así que puedo alucinar 😵‍💫, es tu trabajo corroborar que la respuesta que te entregue sea correcta.")
st.markdown('---')
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("En que te puedo ayudar?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        #Judini
        api_key= os.getenv("JUDINI_API_KEY")
        agent_id= os.getenv("JUDINI_AGENT_ID")
        url = 'https://playground.judini.ai/api/v1/agent/'+agent_id
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer "+api_key}
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data, stream=True)
        raw_data = ''
        tokens = ''
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                raw_data = chunk.decode('utf-8').replace("data: ", '')
                if raw_data != "":
                    lines = raw_data.strip().splitlines()
                    for line in lines:
                        line = line.strip()
                        if line and line != "[DONE]":
                            try:
                                json_object = json.loads(line) 
                                result = json_object['data']
                                full_response += result
                                time.sleep(0.05)
                                # Add a blinking cursor to simulate typing
                                message_placeholder.markdown(full_response + "▌")
                            except json.JSONDecodeError:
                                print(f'Error al decodificar el objeto JSON en la línea: {line}')
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})