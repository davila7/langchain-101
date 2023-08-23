# Deja tu ⭐️ en el repo si te gusta :)

## Aprendiendo Langchain
Tutoriales paso a paso para aprender Langchain con Python en Español
<img width="843" alt="Captura de Pantalla 2023-03-12 a la(s) 5 37 07 p  m" src="https://user-images.githubusercontent.com/6216945/224575138-a1c3e3ad-0831-4717-aae2-ed185f96411d.png">

## Video Tutorial de conceptos básicos

[![Langchain](https://img.youtube.com/vi/6dK0lGjjb08/0.jpg)](https://www.youtube.com/watch?v=6dK0lGjjb08)

## Indice
Guía de estudio para aprender Langchain:

### LLM:
- llm_app.py: Carga un modelo con Langchain
- output_generation.py: Generamos varios resultados de llamadas a OpenAI

### Prompt Templates
- prompt_template.py: Crea un PromptTemplate con variables
- manage_prompt_template.py: Ejecuta un mismo PromptTemplate con diferentes variables
- prompt_from_template.py: Creamos un string con un template y lo cargamos cargamos con from_template()
- prompt_validation.py: Revisamos el parámetro validate_template para validar los inputs del template
- prompt_few_shots.py: Creamos un FewShotPromptTemplate con prefijo, ejemplos y sufijo
- load_prompt.py: Cargamos un prompt template en json y le pasamos variables

### Chat Prompt
- En proceso...

### Memory
- chain_memory.py: Agregamos memoria a una cadena simple usando ConversationChain
- chat_message_history.py: Usamos ChatMessageHistory para ir guardando el historial de mensajes de los usuarios

### Indexes
- pdf_splitter.py: Cargamos un pdf
  
### Chains
- chain.py: Creamos un template y lo asignamos a un chain

### Agents
- agents.py: Creamos un agente que busca en google

### Embeddgins
- En proceso...

### Integraciones
- En Proceso...

# Instalación
Ejecuta estos comandos para instalar las librerías necesarias de la guía de estudio

`pip install langchain`

`pip install openai`

`pip install google-search-results`

Crea el archivo .env y agrega tu API Key de OpenAI y Serpapi API Key

`OPENAI_API_KEY=TU_API_KEY`

`SERPAPI_API_KEY`

Una vez que tengas todo configurado, para ejecutar un archivo solo debes correr el siguiente comando, cambiando el nombre de cada archibo:

`python llm_app.py`

# ¿Cómo comenzar?

1- Realiza un fork o clona este repo en tu pc

2- Sigue la guía de estudio 

3- Dentro de cada archivo encontrarás la descripción de lo que hace el archivo con langchain. 

4- Ejecuta el archivo y revisa lo que la consola te muestra.

5- Cambia el código de cada archivo y realiza diferentes pruebas

6- Repite

# Fuentes

- Langchain: https://langchain.readthedocs.io/en/latest/
- LangChain 101: https://www.youtube.com/watch?v=kYRB-vJFy38

<hr>


Sígueme en Medium: https://medium.com/@dan.avila7

Sígueme en Twitter: https://twitter.com/dani_avila7

Revisa mis videos en Youtube: https://www.youtube.com/channel/UCNabExUbWCar1WvCGWaPNdQ

Instala Code GPT: https://codegpt.co
