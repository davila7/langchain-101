# Import necessary libraries
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and agent ID from environment variables
codegpt_api_key= os.getenv("CODEGPT_API_KEY")
code_gpt_agent_id= os.getenv("CODEGPT_AGENT_ID")

# Set API base URL
codegpt_api_base = "https://api.codegpt.co/v1"

# Create a ChatOpenAI object with the retrieved API key, API base URL, and agent ID
llm = ChatOpenAI(openai_api_key=codegpt_api_key,
                openai_api_base=codegpt_api_base,
                model=code_gpt_agent_id)

# Create a list of messages to send to the ChatOpenAI object
messages = [HumanMessage(content="¿What is Judini?")]

# Send the messages to the ChatOpenAI object and retrieve the response
response = llm(messages)

# Print the response
print(response)
