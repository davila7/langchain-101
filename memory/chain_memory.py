# pip install google-search-results

from dotenv import load_dotenv
from langchain import OpenAI, ConversationChain
import os

'''

En esta archivo agregaremos memoria al llm usando una cadena simple usando ConversationChain

'''

# cargamos openai api key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

llm = OpenAI(temperature=0.9)
conversation = ConversationChain(llm=llm, verbose=True)

# simula una conversación y va guardando en memoria el input del usuario

print(conversation.predict(input="Hola, cómo va todo?"))
print(conversation.predict(input="Todo bien, acá pasando el rato programando"))
print(conversation.predict(input="¿Qué fue lo primero que te dije?"))
print(conversation.predict(input="Dime una frase alternativa a lo primero que te dije."))