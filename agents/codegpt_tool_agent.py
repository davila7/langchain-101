# Import necessary libraries
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
import sys
import io
import re
import os
from typing import Callable, Any
# Tools
from langchain.agents import Tool
from langchain.agents import initialize_agent

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and agent ID from environment variables
codegpt_api_key= os.getenv("CODEGPT_API_KEY")
code_gpt_agent_id= os.getenv("CODEGPT_AGENT_ID")

# Set API base URL
codegpt_api_base = "https://api.codegpt.co/v1"

execute_task_prompt = PromptTemplate(
    template="""Given the following overall question `{input}`.

    Perform the task by understanding the problem, extracting variables, and being smart
    and efficient. Write a detailed response that address the task.
    When confronted with choices, make a decision yourself with reasoning.
    """,
    input_variables=["input"],
)

# Create a ChatOpenAI object with the retrieved API key, API base URL, and agent ID
llm = ChatOpenAI(openai_api_key=codegpt_api_key,
                openai_api_base=codegpt_api_base,
                model=code_gpt_agent_id, verbose=True)
llm_chain = LLMChain(llm=llm, prompt=execute_task_prompt)

danigpt_tool = Tool(
    name='DaniGPT',
    func=llm_chain.run,
    description="Useful for when you need to answer questions about Judini"
) 

# agregamos todos los tools al array
tools = [danigpt_tool]

#memory
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=3,
    return_messages=True
)

llm_openai = ChatOpenAI(model="gpt-4", temperature=0)

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
    st.title("Try CodeGPT Agents as a Tools with Langchain and ReAct 🦜")
    form = st.form('AgentsTools')
    question = form.text_input("Enter your question", "")
    btn = form.form_submit_button("Run")

    if btn:
        st.markdown("### Response Agent AI")
        with st.spinner("Loading"):
            agent = initialize_agent(
                agent="chat-conversational-react-description",
                tools=tools,
                llm=llm_openai,
                verbose=True,
                max_iteration=3,
                early_stop_method="generate",
                memory=memory
            )
            st.info(capture_and_display_output(agent.run, question))


if __name__ == "__main__":
    main()
