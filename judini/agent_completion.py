from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os
import requests

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
    template="Hola cómo estás? mi nombre es {name}",
)

# entregamos la variable name al prompt
print(prompt.format(name="Daniel"))

#Judini
judini_api_key= os.getenv("JUDINI_API_KEY")
agent_id= os.getenv("JUDINI_AGENT_ID")
url = 'https://playground.judini.ai/api/v1/agent/'+agent_id
print(url)
headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer "+judini_api_key}
"""
{
 "messages": [
		{ "role": "user", "content": "Hola" }
	]
}
"""
data = {
    "messages": [
        {
            "role": "user",
            "content": prompt.format(name="Daniel")
        }
    ]
}
print(data)
response = requests.post(url, headers=headers, json=data, stream=True)
print("Status Code:", response.status_code)
raw_data = ''
for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        raw_data += chunk.decode('utf-8')
        print(raw_data)

# raw_data = raw_data.replace("data: ", '')
# raw_data = raw_data.replace("\n", '')
# raw_data = raw_data.replace("[DONE]", '')

# print(raw_data)