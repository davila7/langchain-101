from dotenv import load_dotenv
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI


load_dotenv()


chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
messages = [
    SystemMessage(content="Eres un experto en la historia del futbol"),
    HumanMessage(content="Quién ganó la copa del mundo de Francia 98?")
]
print(messages)
response = chat(messages)

print(response)

