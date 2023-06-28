from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain import ConversationChain
from dotenv import load_dotenv
from langchain.llms import OpenAI
import os

'''

En este archivo creamos el objeto ChatMessageHistory y agregamos mensajes del usuario

Luego creamos el contenedor de ChatMessageHistory que es ConversationBufferMemory para mostrar
los mensajes en una variable

'''

# cargamos openai api key
load_dotenv()

# creamos el objeto history
history = ChatMessageHistory()

# le agregamos mensaje del usuario
history.add_user_message("hi!")
history.add_ai_message("whats up?")
print(history.messages)


# creamos el objeto memory
memory = ConversationBufferMemory()

# agregamos los mensajes
memory.chat_memory.add_user_message("hola, que tal?")
memory.chat_memory.add_ai_message("¿Cómo estás?")
print(memory.load_memory_variables({}))

llm = OpenAI(temperature=0)
conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)

print(conversation.predict(input="Hoy es fin de semana?"))
print(conversation.predict(input="¿Cómo sabes eso?"))