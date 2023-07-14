# pip install google-search-results
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import load_tools, AgentType, initialize_agent, Tool
from langchain import OpenAI, Wikipedia
from langchain.chat_models import ChatOpenAI
from langchain.agents.react.base import DocstoreExplorer
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
import sys
import io
import re
from typing import Callable, Any
# cargamos openai api key
load_dotenv()

def capture_and_display_output(func: Callable[..., Any], *args, **kwargs) -> Any:
    original_stdout = sys.stdout
    sys.stdout = output_catcher = io.StringIO()

    # Ejecutamos la función dada y capturamos su salida
    response = func(*args, **kwargs)

    # Restauramos la salida estándar a su valor original
    sys.stdout = original_stdout

    # Limpiamos la salida capturada
    output_text = output_catcher.getvalue()
    cleaned_text = re.sub(r'\x1b\[[0-9;-]*[mK]', '', output_text)
    lines = cleaned_text.split('\n')
    
    # Mostramos el texto limpiado en Streamlit como código
    with st.expander("Verbose", expanded=True):
        for line in lines:
            st.markdown(line)

    return response

docstore = DocstoreExplorer(Wikipedia())
agents = []
n_tools = ["serpapi", "llm-math", "arxiv", "wolfram-alpha", "human", "requests_all", "openweathermap-api"]
docstore_tools = ["search", "lookup"]
conversational_tools = ['current_search']
self_ask_tools = ['intermediate_answer']

# ejecutamos el agente
def main():
    chat_agent = False
    load_tools_boolean = True
    memory = None
    st.set_page_config(page_title="Langchain Agent AI", page_icon="🤖", layout="wide")
    st.title("Try Langchain Agents 🦜")
    for key in AgentType:
        agents.append(key.value)
        
    options_agent = st.selectbox(
    'Select Agents',
    agents)


    if options_agent == 'zero-shot-react-description':
        st.write(options_agent, ": This agent uses the ReAct framework to determine which tool to use based solely on the tool's description. Any number of tools can be provided. This agent requires that a description is provided for each tool.")
        tools = n_tools

    if options_agent == 'react-docstore':
        st.write(options_agent, ": This agent uses the ReAct framework to interact with a docstore. Two tools must be provided: a Search tool and a Lookup tool (they must be named exactly as so). The Search tool should search for a document, while the Lookup tool should lookup a term in the most recently found document. This agent is equivalent to the original ReAct paper, specifically the Wikipedia example.")
        tools = docstore_tools
        load_tools_boolean = False
    
    if options_agent == 'self-ask-with-search':
        st.write(options_agent, ": This agent utilizes a single tool that should be named Intermediate Answer. This tool should be able to lookup factual answers to questions. This agent is equivalent to the original self ask with search paper, where a Google search API was provided as the tool.")
        tools = self_ask_tools
        load_tools_boolean = False

    if options_agent == 'conversational-react-description':
        st.write(options_agent, ": This agent is designed to be used in conversational settings. The prompt is designed to make the agent helpful and conversational. It uses the ReAct framework to decide which tool to use, and uses memory to remember the previous conversation interactions.")
        tools = conversational_tools
        memory = ConversationBufferMemory(memory_key="chat_history")
        load_tools_boolean = False
    
    if options_agent == 'chat-zero-shot-react-description':
        st.write(options_agent, ": This agent uses the ReAct framework to determine which tool to use based solely on the tool's description. Any number of tools can be provided. This agent requires that a description is provided for each tool.")
        tools = n_tools
        chat_agent = True
    
    if options_agent == 'chat-conversational-react-description':
        st.write(options_agent, ": The chat-conversational-react-description agent type lets us create a conversational agent using a chat model instead of an LLM")
        tools = conversational_tools
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        load_tools_boolean = False
        chat_agent = True

    if options_agent == 'openai-functions':
        st.write(options_agent, ": Certain OpenAI models (like gpt-3.5-turbo-0613 and gpt-4-0613) have been explicitly fine-tuned to detect when a function should to be called and respond with the inputs that should be passed to the function. The OpenAI Functions Agent is designed to work with these models.")
        tools = n_tools
        chat_agent = True

    if options_agent == 'openai-multi-functions':
        st.write(options_agent, ": Certain OpenAI models (like gpt-3.5-turbo-0613 and gpt-4-0613) have been explicitly fine-tuned to detect when a function should to be called and respond with the inputs that should be passed to the function. The OpenAI Functions Agent is designed to work with these models.")
        tools = n_tools
        chat_agent = True
        
    
    tools_selected = st.multiselect(
    'Select Tools',
    tools)

    if "search" in tools_selected:
        tools_selected.remove("search")
        tools_selected.append(
            Tool(
                name="Search",
                func=docstore.search,
                description="useful for when you need to ask with search",
            ))
    if "lookup" in tools_selected:
        tools_selected.remove("lookup")
        tools_selected.append(
            Tool(
                name="Lookup",
                func=docstore.lookup,
                description="useful for when you need to ask with lookup",
            ))
        
    if "current_search" in tools_selected:
        tools_selected.remove("current_search")
        search = SerpAPIWrapper()
        tools_selected.append(
            Tool(
                name = "Current Search",
                func=search.run,
                description="useful for when you need to answer questions about current events or the current state of the world"
            ),
        )

    if "intermediate_answer" in tools_selected:
        tools_selected.remove("intermediate_answer")
        search = SerpAPIWrapper()
        tools_selected.append(
            Tool(
                name="Intermediate Answer",
                func=search.run,
                description="useful for when you need to ask with search",
            )
        )

    st.write('Tools', tools_selected)
    form = st.form('AgentsTools')
    question = form.text_input("Enter your question", "")
    btn = form.form_submit_button("Run")

    if btn:
        st.markdown("### Response Agent AI")
        with st.spinner("Loading"):

            if chat_agent:
                llm = ChatOpenAI(temperature=0, model="gpt-4-0613")
            else:
                llm = OpenAI(temperature=0)


            if load_tools_boolean:
                final_tools = load_tools(tools_selected, llm)
            else:
                final_tools = tools_selected

            
            agent = initialize_agent(final_tools, llm, agent=options_agent, verbose=True, memory=memory)
            
            
            st.info(capture_and_display_output(agent.run, question))

if __name__ == "__main__":
    main()