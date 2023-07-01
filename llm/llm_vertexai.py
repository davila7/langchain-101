from dotenv import load_dotenv
from langchain.llms import VertexAI
import os

"""
VertexAI
"""

load_dotenv()
llm = VertexAI()


text = "Hi"
print(llm(text))
