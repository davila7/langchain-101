from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os

# load openai api key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = OpenAI(temperature=0.9)

prompt = PromptTemplate(
    input_variables=["name"],
    template="Hola cómo estás? mi nombre es {name}",
)

# mismo template, diferente variables
print(llm(prompt.format(name="Daniel")))
print(llm(prompt.format(name="José")))
