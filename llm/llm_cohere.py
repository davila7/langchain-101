from dotenv import load_dotenv
from langchain.llms import Cohere
import os

"""
Cohere
"""

# cargamos apikey
load_dotenv()

# creamos el modelo con temperatura 0.9
llm = Cohere(temperature=0.3)

# entregamos la variable text como variable al modelo
text = "Who won the FIFA World Cup in the year 1998?"
print(llm(text))
