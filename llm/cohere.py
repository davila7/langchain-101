from dotenv import load_dotenv
from langchain.llms import Cohere
import os

"""
Cohere

"""

# cargamos apikey
load_dotenv()
cohere_api_key = os.getenv("cohere_api_key")
os.environ["cohere_api_key"] = cohere_api_key

# creamos el modelo con temperatura 0.9
llm = Cohere(cohere_api_key=cohere_api_key, temperature=0.9)

# entregamos la variable text como variable al modelo
text = "Hola cómo estás?"
print(llm(text))
