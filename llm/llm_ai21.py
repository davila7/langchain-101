from dotenv import load_dotenv
from langchain.llms import AI21
import os

"""
AI21

"""

# cargamos apikey
load_dotenv()
llm = AI21(temperature=0.9)

# entregamos la variable text como variable al modelo
text = "Hola cómo estás?"
print(llm(text))
