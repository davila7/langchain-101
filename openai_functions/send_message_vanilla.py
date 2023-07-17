import os
import openai
import json

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pywhatkit as pwk
import streamlit as st
from dotenv import load_dotenv
import datetime

load_dotenv()

def send_whatsapp(person, message):
    print(person)
    print(message)
    number = ''
    if(person == 'PERSONA'):
        number = 'NUMERO_PERSONA'
    
    # sending message in Whatsapp in India so using Indian dial code (+91)
    if(number != ''):
        now = datetime.datetime.now()
        minutes = now.minute+1
        print(minutes)
        pwk.sendwhatmsg(number, message, now.hour, minutes)
    

def send_email(email, subject, body):
    """send the user an email with the answer"""

    #try:
    
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

    # except Exception as e:
    #     print(f"An error occurred: {str(e)}")


openai.api_key = os.getenv("OPENAI_API_KEY")
def run_conversation(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "user", "content": prompt}],
        functions=[
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
            },
            {
                "name": "send_whatsapp",
                "description": "Sends an whatsapp to the specified person",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "person": {
                            "type": "string",
                            "description": "A person to send the whatsapp",
                        },
                        "whatsapp_message": {"type": "string"},
                    },
                },
            }
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]
    st.write(message)

    # Step 2, check if the model wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        print('function_name: ', function_name)

        if(function_name == 'send_email'):
            # Access the arguments
            arguments = json.loads(message['function_call']['arguments'])
            email_arg = arguments['email']
            body_arg = arguments['body']
            subject_arg = arguments['subject']

            # Step 3, call the function
            function_response = send_email(
                email_arg, subject_arg, body_arg
            )

            print(function_response)

        if(function_name == 'send_whatsapp'):
            # Access the arguments
            arguments = json.loads(message['function_call']['arguments'])
            person_arg = arguments['person']
            message_arg = arguments['whatsapp_message']

            # Step 3, call the function
            function_response = send_whatsapp(
                person_arg, message_arg
            )

            print(function_response)

def main():
    st.set_page_config(page_title="Langchain Agent AI", page_icon="🤖", layout="wide")
    st.title("Try OpenAI Function Callings 🦜")
    st.write(send_email)
    st.write(send_whatsapp)
    form = st.form('AgentsTools')
    question = form.text_input("Enter your question", "")
    btn = form.form_submit_button("Run")

    if btn:
        st.markdown("### Response Agent AI")
        with st.spinner("Loading"):
               
            run_conversation(question)


if __name__ == "__main__":
    main()