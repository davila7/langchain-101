from dotenv import load_dotenv
from langchain import HuggingFaceHub
from langchain import PromptTemplate, LLMChain
import os

"""
HuggingFace falcon

"""
# cargamos apikey
load_dotenv()

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm = HuggingFaceHub(repo_id='tiiuae/falcon-7b-instruct', model_kwargs={"temperature":0.3})
llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "Who won the FIFA World Cup in the year 1998?"
print(question)
print('Falcon: ', llm_chain.run(question))

