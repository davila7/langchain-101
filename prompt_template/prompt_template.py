from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os

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
print(prompt.format(name="Fernando"))

# cargamos dentro del modelo el prompt con la variable como parametro
print(llm(prompt.format(name="Fernando")))