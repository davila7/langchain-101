from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os

# cargamos openai api key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = OpenAI(temperature=0.9)

prompt = PromptTemplate(
    input_variables=["name"],
    template="Hola cómo estás? mi nombre es {name}",
)

# usamos el mismo template con diferentes variables

# ejemplo con variable name = Daniel
print(prompt.format(name="Daniel"))
print(llm(prompt.format(name="Daniel")))

# ejemplo con variable name = José
print(prompt.format(name="José"))
print(llm(prompt.format(name="José")))
