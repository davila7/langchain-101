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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = OpenAI(temperature=0.9)

# prompt template con una variables
prompt = PromptTemplate(
    input_variables=["name"],
    template="Hola cómo estás? mi nombre es {name}",
)

# entregamos la variable name al prompt
print(prompt.format(name="Daniel"))

# cargamos dentro del modelo el prompt con la variable como parametro
print(llm(prompt.format(name="Daniel")))