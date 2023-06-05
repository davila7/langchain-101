from dotenv import load_dotenv
from langchain.llms import AI21
import os

"""
AI21

"""

# cargamos apikey
load_dotenv()
AI21_API_KEY = os.getenv("AI21_API_KEY")
llm = AI21(ai21_api_key=AI21_API_KEY)

# entregamos la variable text como variable al modelo
text = "Hola cómo estás?"
print(llm(text))
