from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

# cargamos openai api key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# creamos el modelo con temperatura 0.9
llm = OpenAI(temperature=0.9)

# entregamos la variable text como variable al modelo
text = "Hola cómo estás?"
print(llm(text))
