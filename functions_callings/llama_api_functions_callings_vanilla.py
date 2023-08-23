import json
from llamaapi import LlamaAPI
from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import streamlit as st
import asyncio
from pydantic import BaseModel
from typing import List

load_dotenv()

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class FunctionCallArguments(BaseModel):
    email: str
    body: str
    subject: str

class FunctionCall(BaseModel):
    name: str
    arguments: FunctionCallArguments

class Message(BaseModel):
    function_call: FunctionCall

class Choice(BaseModel):
    message: Message

class ChoiceList(BaseModel):
    choices: List[Choice]

def send_email(email, subject, body):
    """send the user an email with the answer"""

    try:
        if(subject == ''):
                subject = 'GPT Email'
        message = Mail(
            # add the email connected to your sendgrid code here
            from_email=os.getenv("SENDGRID_EMAIL"),
            to_emails=email,
            subject=subject,
            html_content=body
        )    
        st.write(message)
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        st.write(response)

    except Exception as e:
        st.write(f"An error occurred: {str(e)}")


# Define your API request
def run_conversation(prompt):
    # Initialize the llamaapi with your api_token
    llama = LlamaAPI(os.getenv("LLAMA_API_API_KEY"))
    function_calling_json = [
            {
                "name": "send_email",
                "description": "Sends an email to the specified email address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "An email address to send the email to",
                        },
                        "body": {"type": "string"},
                        "subject": {"type": "string"},
                    },
                },
            }
        ]

    api_request_json = {
    "messages": [
        {"role": "user", "content": prompt},
    ],
    "functions": function_calling_json,
    "stream": False,
    "function_call": "auto"
    }

    # Make your request and handle the response
    response = llama.run(api_request_json)
    message = response.json()
    st.write(message)

    # Step 2, check if the model wants to call a function
    if message['choices'][0]['message']['function_call']:
        function_name = message['choices'][0]['message']['function_call']["name"]
        st.write(function_name)
        if(function_name == 'send_email'):
            # Access the arguments
            model = ChoiceList(**message)
            arguments = model.choices[0].message.function_call.arguments
            st.write(arguments)
            email_arg = arguments.email
            body_arg = arguments.body
            subject_arg = arguments.subject

            # Step 3, call the function
            function_response = send_email(
                email_arg, subject_arg, body_arg
            )

            print(function_response)

def main():
    st.set_page_config(page_title="Llama API Function Callings", page_icon="🤖", layout="wide")
    st.title("Llama API Function Callings 🦙")
    form = st.form('AgentsTools')
    question = form.text_input("Instruction", "")
    btn = form.form_submit_button("Run")

    if btn:
        st.markdown("### Response Llama API")
        with st.spinner("Loading"):   
            run_conversation(question)


if __name__ == "__main__":
    main()