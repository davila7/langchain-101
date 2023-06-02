from langchain.prompts import load_prompt


"""
7.- Load Prompt

En este archivo vamos a cargar un template en formato json (puede ser yml también)
y luego vamos a pasarle las variables con format()

"""


prompt = load_prompt("./files/simple_prompt.json")
print(prompt.format(name="Daniel", time="tardes"))
