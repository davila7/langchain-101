import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(email, subject, body):
    """send the user an email with the answer"""

    try:
        if(subject == ''):
            subject = 'GPT Email'
        message = Mail(
            # add the email connected to your sendgrid code here
            from_email='daniel@judini.ai',
            to_emails=email,
            subject=subject,
            html_content=body
        )    
        st.write(message)
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        
        response = sg.send(message)
        st.write(response.status_code)
        st.write(response.body)
        st.write(response.headers)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

st.title('GPT Sends Emails')
st.write('Instructions:')
st.write("Click on the 'Start Talking' button and allow the browser permission to use the microphone. Say a sentence requesting to send an email with a message. You must say the person's full email address.")
st.write("Example: Send an email to dan.avila7@gmail.com reminding him that he must study the OpenAI Functions API for tomorrow's exam")
user_secret = st.text_input(label = ":blue[OpenAI API key]",
                                value="",
                                placeholder = "Paste your openAI API key, sk-",
                                type = "password")
if(user_secret):
    stt_button = Button(label="Start talking", button_type="success")
    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
    
        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if ( value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
        """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        user_input = result.get("GET_TEXT")
        st.write('Audio Input: ', user_input)
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": user_input}],
            functions=[
                {
                    "name": "send_email",
                    "description": "Sends an email to a person",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "email": {
                                "type": "string",
                                "description": "A person to send the email",
                            },
                            "body": {"type": "string"},
                            "subject": {"type": "string"},
                        },
                    },
                }
            ],
            function_call="auto",
        )
        message = response["choices"][0]["message"]
    
    st.write('GPT: ', message)

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