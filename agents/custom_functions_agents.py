# Configuración normal
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.callbacks import StreamlitCallbackHandler
import sys
import io
import re
from typing import Callable, Any

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

def obtiene_tiempo(lugar):
    #llamado a la api wheater
    # POST como parametro el pais
    return "No podemos acceder al clima en "+lugar

# Creo el tool
nombre_tool = Tool(
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
tools = [search, nombre_tool, timepo_tool]

#memory
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=3,
    return_messages=True
)

def capture_and_display_output(func: Callable[..., Any], *args, **kwargs) -> Any:
    original_stdout = sys.stdout
    sys.stdout = output_catcher = io.StringIO()

    # Ejecutamos la función dada y capturamos su salida
    # response = func(*args, **kwargs)
    st_callback = StreamlitCallbackHandler(st.container(), max_thought_containers=100, expand_new_thoughts=True, collapse_completed_thoughts=False)
    response = func(*args, callbacks=[st_callback])

    # Restauramos la salida estándar a su valor original
    sys.stdout = original_stdout

    # Limpiamos la salida capturada
    output_text = output_catcher.getvalue()
    cleaned_text = re.sub(r'\x1b\[[0-9;-]*[mK]', '', output_text)
    lines = cleaned_text.split('\n')
    
    # Mostramos el texto limpiado en Streamlit como código
    with st.expander("Verbose", expanded=False):
        for line in lines:
            st.markdown(line)

    return response


def main():
    st.set_page_config(page_title="Langchain Agent AI", page_icon="🤖", layout="wide")
    st.title("Try Custom Langchai Agents 🦜")
    form = st.form('AgentsTools')
    question = form.text_input("Enter your question", "")
    btn = form.form_submit_button("Run")

    if btn:
        st.markdown("### Response Agent AI")
        with st.spinner("Loading"):
            
            agent = initialize_agent(
                agent="chat-conversational-react-description",
                tools=tools,
                llm=turbo_llm,
                verbose=True,
                max_iteration=3,
                early_stop_method="generate",
                memory=memory
            )
            st.info(capture_and_display_output(agent.run, question))


if __name__ == "__main__":
    main()