from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os
import requests
import json

"""
2.- Prompt Template

En este archivo cargamos un template con variables que se entregan mediante inputs.
Luego de crear el template podemos mostrar enviar la variable con format() y visualizar el template
antes de enviarlo a la API

"""

# cargamos openai api key
load_dotenv()

llm = OpenAI(temperature=0.9)

# prompt template con una variables
prompt = PromptTemplate(
    input_variables=["name"],
    template="Hola, mi nombre es {name}",
)

#Judini
judini_api_key= os.getenv("JUDINI_API_KEY")
agent_id= os.getenv("JUDINI_AGENT_ID")
url = 'https://playground.judini.ai/api/v1/agent/'+agent_id
headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer "+judini_api_key}
data = {
    "messages": [
        {
            "role": "user",
            "content": prompt.format(name="Daniel")
        }
    ]
}
#print(data)
response = requests.post(url, headers=headers, json=data, stream=True)
raw_data = ''
tokens = ''
for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        raw_data = chunk.decode('utf-8').replace("data: ", '')
        if raw_data != "":
            lines = raw_data.strip().splitlines()
            for line in lines:
                print(line)
                line = line.strip()
                if line and line != "[DONE]":
                    try:
                        json_object = json.loads(line)
                        print('json_ok')
                        result = json_object['data']
                        result = result.replace("\n", "")
                        tokens += result
                    except json.JSONDecodeError:
                        print(f'Error al decodificar el objeto JSON en la línea: {line}')
            
print(tokens)