import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()

# Setting page title and header
st.set_page_config(page_title="Judini", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Judini Agent 🤖</h1>", unsafe_allow_html=True)

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Sidebar
st.sidebar.title("Sidebar")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

#Judini
judini_api_key= os.getenv("JUDINI_API_KEY")
agent_id= os.getenv("JUDINI_AGENT_ID")
url = 'https://playground.judini.ai/api/v1/agent/'+agent_id
headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer "+judini_api_key}


# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    token = ''
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            raw_data = chunk.decode('utf-8').replace("data: ", '')
            if raw_data != "[DONE]":
                try:
                    json_object = json.loads(raw_data.strip())
                    token += json_object['data']
                except json.JSONDecodeError as e:
                    print(f"Error al cargar el JSON: {e}")
    response = token
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = 0
    prompt_tokens = 0
    completion_tokens = 0
    return response, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))