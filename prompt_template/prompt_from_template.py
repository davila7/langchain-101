from langchain.prompts import PromptTemplate

"""
4.- Prompt from template

En este archivo primero crearemos el template, luego lo cargaremos en el PromptTamplete
y luego le entregaremos las variables

"""

template = "Hola buenos {time}, mi nombre es {name}."

prompt_template = PromptTemplate.from_template(template)

# mostramos las variables
print(prompt_template.input_variables)

# En este ejemplo pasamos multiples variables al template
print(prompt_template.format(time="noches", name="José"))
