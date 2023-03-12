from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=0.9)

text = "Hola cómo estás?"
print(llm(text))
