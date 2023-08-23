from judini.agent import Agent
import os
from dotenv import load_dotenv
from judini.agent import Agent
load_dotenv()

api_key= os.getenv("JUDINI_API_KEY")
agent_id= os.getenv("JUDINI_AGENT_ID")

agent = Agent(api_key, agent_id)

prompt = 'Hola, cómo estás?'
response = agent.completion(prompt)
print(response) 