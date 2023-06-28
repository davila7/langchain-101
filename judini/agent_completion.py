from judini.agent import Agent

api_key= "JUDINI_API_KEY"
agent_id= "JUDINI_AGENT_ID"

agent = Agent(api_key, agent_id)

prompt = 'Quien es el presidente de Chile?'
response = agent.completion(prompt)
print(response) 