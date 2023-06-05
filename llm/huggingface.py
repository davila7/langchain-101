from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from dotenv import load_dotenv
import os

"""
HuggingFace falcon

"""


# cargamos apikey
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

template = '''
Question: {question}
Answer: Let's think step by step.
'''

prompt = PromptTemplate(template=template, input_variables=['question'])
llm = HuggingFaceHub(repo_id='tiiuae/falcon-7b-instruct', model_kwargs={"temperature":0.3})

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "Who is your creator?"
print(question)
print('Falcon: ', llm_chain.run(question))

