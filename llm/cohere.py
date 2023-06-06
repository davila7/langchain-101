from dotenv import load_dotenv
from langchain.llms import Cohere
import os

"""
Cohere

"""

# cargamos apikey
load_dotenv()

# creamos el modelo con temperatura 0.9
llm = Cohere(temperature=0.9)

# entregamos la variable text como variable al modelo
text = "Hola cómo estás?"
print(llm(text))
