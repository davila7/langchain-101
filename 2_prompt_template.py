from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os

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
#print(llm(prompt.format(name="Daniel")))


# En este ejemplo pasamos multiples variables al template
multiple_input_prompt = PromptTemplate(
    input_variables=["time", "name"], 
    template="Hola buenos {time}, mi nombre es {name}."
)
print(multiple_input_prompt.format(time="noches", name="José"))