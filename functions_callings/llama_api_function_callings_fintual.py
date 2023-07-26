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
import requests
import matplotlib.pyplot as plt
import datetime
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

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
    fondo_name: str
    date_from: str
    date_to: str

class FunctionCall(BaseModel):
    name: str
    arguments: FunctionCallArguments

class Message(BaseModel):
    function_call: FunctionCall

class Choice(BaseModel):
    message: Message

class ChoiceList(BaseModel):
    choices: List[Choice]

def api_fintual(fondo, from_date, to_date):
    """ id, from_date, to_date """
    id=15077
    if fondo == "Very Conservative Streep":
        id = 15077
    if fondo == "Conservative Clooney":
        id = 188
    if fondo == "Moderate Pit":
        id = 187
    if fondo == "Risky Norris":
        id = 186

    url = 'https://fintual.cl/api/real_assets/'+str(id)+'/days?from_date='+from_date+'&to_date='+to_date

    response = requests.get(url)
    json_response = response.json()
    st.write(json_response)

    dates = [item["attributes"]["date"] for item in json_response["data"]]
    prices = [item["attributes"]["price"] for item in json_response["data"]]

    plt.figure(figsize=(10,5))
    plt.bar(dates, prices, color = 'blue')

    plt.xlabel('Fecha')
    plt.ylabel('Precio')
    plt.title('Precio por Fecha')
    plt.xticks(rotation=90) 

    st.pyplot(plt)

    # luego de pintar los datos vamos a hacer que el modelo revise y entregue una conclusion de los datos obtenidos
    llm = OpenAI(temperature=0)
    tools = load_tools(["llm-math"], llm=llm)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    prompt = PromptTemplate(
        input_variables=["fondo", "dates", "prices"],
        template='''
            Actúa como un experto en administradoras de fondos mutuos y analiza los siguientes datos:

            Fondo:{fondo}
            Fechas: {dates}
            Precios: {prices}
            
            Entrega una conclusión de cómo se ha ido comportando el fondo y un consejo al usuario de si debe seguir invirtiendo o retirar fondos
            ''',
    )
    response_agent = agent.run(prompt.format(fondo=fondo, dates=dates, prices=prices))
    st.info(response_agent)



    


# Define your API request
def run_conversation(prompt):
    # Initialize the llamaapi with your api_token
    llama = LlamaAPI(os.getenv("LLAMA_API_API_KEY"))
    function_calling_json = [
            {
                "name": "get_fondo_data",
                "description": "útil cuando un usuario quiere preguntar sobre fondos de desde un rango específico",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fondo_name": {
                            "type": "string",
                            "description": "nombre del fondo",
                        },
                        "date_from": {
                            "type": "string",
                            "description":"Fecha desde cuando se quiere consultar"
                        },
                        "date_to": {
                            "type": "string",
                            "description":"Fecha hasta cuando se quiere consultar"
                        },
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
        if(function_name == 'get_fondo_data'):
            # Access the arguments
            model = ChoiceList(**message)
            arguments = model.choices[0].message.function_call.arguments
            st.write(arguments)

            # Step 3, call the function
            function_response = api_fintual(
                arguments.fondo_name, arguments.date_from, arguments.date_to
            )

            print(function_response)

def main():
    st.set_page_config(page_title="Llama 2 API Function Callings Fintual", page_icon="🤖", layout="wide")
    st.title("Llama 2 API Function Callings 🦙 Fintual")
    st.write('Fondos:')
    st.write('Very Conservative Streep: casi pura renta fija. id: 15077')
    st.write('Conservative Clooney: principalmente renta fija. id: 188')
    st.write('Moderate Pit: la justa mezcla de renta fija y ETFs accionarios. id: 187')
    st.write('Risky Norris: casi solamente ETFs accionarios. id: 186')
    form = st.form('AgentsTools')
    question = form.text_input("Instruction", "")
    btn = form.form_submit_button("Run")

    if btn:
        st.markdown("### Response Llama API")
        with st.spinner("Loading"):   
            run_conversation(question)


if __name__ == "__main__":
    main()