from langchain import PromptTemplate, FewShotPromptTemplate

"""
6.- Few Shot prompt template

En este archivo armaremos un Few Shot prompt template, que permitirá armar un template con pequeños ejemplos e instrucciones para que el LLM tenga el contexto de lo que necesitamos.

"""

# creamos una lista de ejemplos
examples = [
    {"name": "Daniel", "time": "días"},
    {"name": "José", "time": "tardes"},
]

# creamos el formato del ejemplo que vamos a entregar
example_formatter_template = """Mi nombre es {name}
, buenos {time}
"""

# creamos el template de ejemplo
example_prompt = PromptTemplate(
    input_variables=["name", "time"],
    template=example_formatter_template,
)

# Creamos el objeto `FewShotPromptTemplate`
few_shot_prompt = FewShotPromptTemplate(
    # le pasamos el array de palabras de ejemplo
    examples=examples,
    # le pasamos el formato del ejemplo con el template
    example_prompt=example_prompt,
    # El prefix es una instrucción para que el LLM sepa que debe hacer con estos ejemplos
    prefix="Genera frases con nombres y saludos\n",
    # El suffix es donde se agrega el input del usuario para generar el texto que sigue
    suffix="Hola mi nombre es Fernando, buenas {input}",
    # indicamos la variable que se agregará al template
    input_variables=["input"],
    # string separador entre el prefix, examples y el suffix
    example_separator="\n",
)

# Generamos el prompt con la función format()
print(few_shot_prompt.format(input="noches"))
