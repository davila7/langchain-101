from langchain.prompts import PromptTemplate

"""
5.- Prompt validation

En este archivo creamos un prompt template con más inputs del que el string inicial soporta
Podemos activar o desactivar la validación de variables dentro del template

"""

template = "Mi nombre es {name}."

# error por enviar más variables de las que tiene el template
# prompt_template = PromptTemplate(template=template, 
#                                  input_variables=["name", "foo"]) 

# desactivamos el error con validate_template = False
prompt_template = PromptTemplate(template=template, 
                                 input_variables=["name", "foo"], 
                                 validate_template=False) # No muestra el error

print(prompt_template.format(name="Daniel"))
