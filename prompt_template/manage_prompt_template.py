from langchain.prompts import PromptTemplate

"""
3.- Manage Prompt Template

En este archivo creamos un template con multiples variables y se las entregamos mediante dos inputs
con el format()

"""

# En este ejemplo pasamos multiples variables al template
multiple_input_prompt = PromptTemplate(
    input_variables=["time", "name"], 
    template="Hola buenos {time}, mi nombre es {name}."
)

print(multiple_input_prompt.format(time="noches", name="José"))
