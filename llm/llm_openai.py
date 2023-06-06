from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

"""
1.- LLM App

En este archivo estamos cargando las variables de entorno desde el archivo .env
Luego creamos un modelo con Langchain solo con un parámetro (temperature=0.9) y luego 
le pasamos un texto al llm para que se haga el llamado a la API de OpenAI

"""

# cargamos openai api key
load_dotenv()

# creamos el modelo con temperatura 0.9
llm = OpenAI(temperature=0.9)

# entregamos la variable text como variable al modelo
text = "Hola cómo estás?"
print(llm(text))
