from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import os

"""

 En este archivo creamos dos cadenas con que reciben una misma variable y las unimos con SimpleSequentialChain para luego ejecutar todas las cadenas unidas

"""


# cargamos openai api key
load_dotenv()

# cargamos el modelo
llm = OpenAI(temperature=0.9)

# Chain 1
# creamos el primer string del template
template = "Eres un experto en programación, explica cómo se inicializa una variable en {language}."
# cargamos el primer template con las variables
prompt_template = PromptTemplate(template=template, input_variables=['language'])
# creamos el primer chain con el saludo
var_chain = LLMChain(llm=llm, prompt=prompt_template)

# Chain 2
# creamos el segundo string del template
template = "Eres un experto en programación, explica cómo se realiza un loop en {language}."
# cargamos el segundo template con las variables
prompt_template = PromptTemplate(template=template, input_variables=['language'])
# creamos el segundo chain con el saludo
loop_chain = LLMChain(llm=llm, prompt=prompt_template)


# ya tenemos las dos cadenas creadas, ahora las ejecutamos
from langchain.chains import SimpleSequentialChain
conversa_chain = SimpleSequentialChain(chains=[var_chain, loop_chain], verbose=True)
conversa_chain.run('javascript')

'''
> Entering new SimpleSequentialChain chain...

Inicializar una variable en Javascript es el proceso de asignarle un valor a una variable. Esto se realiza mediante la instrucción "let" para crear una variable y la instrucción "= " para asignarle un valor. Por ejemplo, el siguiente código muestra cómo inicializar una variable llamada "nombre" con un valor de "Juan". 

let nombre = "Juan";
 

Un loop es una estructura de control en la que una instrucción o un conjunto de instrucciones se ejecutan repetidamente mientras se cumplen ciertas condiciones. Existen diferentes tipos de loops en Javascript, incluyendo for, for/in, while, do/while, y for/of. El loop for es el más comúnmente usado. 

El siguiente código muestra cómo crear un loop for en Javascript. Por ejemplo, se puede utilizar para recorrer una matriz y realizar una acción para cada elemento de la matriz. 

let matriz = [1,2,3,4,5];
for (let i = 0; i < matriz.length; i++) { 
  console.log(matriz[i]); // Imprime 1, 2, 3, 4, 5
}
> Finished chain.
'''