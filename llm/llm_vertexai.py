from dotenv import load_dotenv
from langchain.llms import VertexAI
import os

"""
VertexAI

"""

# cargamos apikey
load_dotenv()
llm = VertexAI()

# entregamos la variable text como variable al modelo
text = "Hola cómo estás?"
print(llm(text))
