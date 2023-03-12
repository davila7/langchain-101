from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

# load openai api key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = OpenAI(temperature=0.9)

text = "Hola cómo estás?"
print(llm(text))
