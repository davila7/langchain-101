# Configuración normal
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# cargamos openai api key
load_dotenv()

# Tools
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent

turbo_llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo"
)

# Tools para buscar en internet una pregunta
search = DuckDuckGoSearchRun()

# Así agregamos tools por defecto de langchain
tools = [
    Tool(
        name= "search",
        func= search.run,
        description= "útil cuando necesitas buscar respuestas sobre un tema en especifico"
    )
]

# Tools custom
# Así agregamos un tools creado por nosotros
def extrae_nombre(name):
    return "El nombre es "+name

def obtiene_tiempo(pais):
    #llamado a la api wheater
    # POST como parametro el pais
    return "el tiempo es "+pais

# Creo el tool
suma_tool = Tool(
    name= "extrae_nombre",
    func=extrae_nombre,
    description="útil cuando queremos saber el nombre de una persona que participa en una conversación, input debería ser el primer nombre"
)

# Obtener el tiempo de un pais
timepo_tool = Tool(
    name= "tiempo",
    func=obtiene_tiempo,
    description="útil cuando queremos saber el tiempo de un determinado pais, el input debe ser el nombre del pais"
)

# agregamos todos los tools al array
tools = [search, suma_tool, timepo_tool]

#memory
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=3,
    return_messages=True
)

conversational_agent = initialize_agent(
    agent="chat-conversational-react-description",
    tools=tools,
    llm=turbo_llm,
    verbose=True,
    max_iteration=3,
    early_stop_method="generate",
    memory=memory
)

#conversational_agent("Daniel Ávila está participando de una conversación, cuál es su primer nombre?")

conversational_agent("está lloviendo en Chile?")