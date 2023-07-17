from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)
load_dotenv()

chat = ChatOpenAI(model="gpt-4",temperature=0)
messages = [
    HumanMessage(content="¿Cuánto es 4.1 ^ 2.1?")
]

response = chat(messages)
print(response)