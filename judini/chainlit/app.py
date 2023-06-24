import chainlit as cl
import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()

#Judini
judini_api_key= os.getenv("JUDINI_API_KEY")
agent_id= os.getenv("JUDINI_AGENT_ID")
url = 'https://playground.judini.ai/api/v1/agent/'+agent_id
headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer "+judini_api_key}


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful AI assistant."}],
    )



@cl.on_message
async def main(message: str):
    data = {
        "messages": [
            {
                "role": "user",
                "content": message
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
                    print(4)
                    json_object = json.loads(raw_data.strip())
                    token += json_object['data']
                except json.JSONDecodeError as e:
                    print(5)
                    print(f"Error al cargar el JSON: {e}")
    await cl.Message(
        content=token,
    ).send()

    