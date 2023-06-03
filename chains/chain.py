from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os

"""

En este archivo creamos un template y luego ejecutamos una simple cadena con LLMChain

"""


# cargamos openai api key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# cargamos el modelo
llm = OpenAI(temperature=0.9)

# creamos el template
prompt = PromptTemplate(
    input_variables=["name"],
    template="Hola cómo estás? mi nombre es {name}",
)

# creamos un chain y le entregamos como parámetro el modelo y el prompt template
chain = LLMChain(llm=llm, prompt=prompt)

# ejecutamos la cadena con el parametro name = Fernando
print(chain.run("Fernando"))
