import streamlit as st
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, String, Table, Date, Float
from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import Tool
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from sqlalchemy import create_engine
from sqlalchemy import insert
import sys
import io
import re
from typing import Callable, Any
load_dotenv()

#Cuenta los tokens
def count_tokens(agent, query):
    with get_openai_callback() as cb:
        result = agent(query)
        print(f'Spent a total of {cb.total_tokens} tokens')

    return result

llm = ChatOpenAI(model="gpt-4", temperature=0)


metadata_obj = MetaData()

stocks = Table(
    "stocks",
    metadata_obj,
    Column("obs_id", Integer, primary_key=True),
    Column("stock_ticker", String(4), nullable=False),
    Column("price", Float, nullable=False),
    Column("date", Date, nullable=False),    
)

engine = create_engine("sqlite:///:memory:")
metadata_obj.create_all(engine)

observations = [
    [1, 'ABC', 200, datetime(2023, 1, 1)],
    [2, 'ABC', 208, datetime(2023, 1, 2)],
    [3, 'ABC', 232, datetime(2023, 1, 3)],
    [4, 'ABC', 225, datetime(2023, 1, 4)],
    [5, 'ABC', 226, datetime(2023, 1, 5)],
    [6, 'XYZ', 810, datetime(2023, 1, 1)],
    [7, 'XYZ', 803, datetime(2023, 1, 2)],
    [8, 'XYZ', 798, datetime(2023, 1, 3)],
    [9, 'XYZ', 795, datetime(2023, 1, 4)],
    [10, 'XYZ', 791, datetime(2023, 1, 5)],
]

def insert_obs(obs):
    stmt = insert(stocks).values(
    obs_id=obs[0], 
    stock_ticker=obs[1], 
    price=obs[2],
    date=obs[3]
    )

    with engine.begin() as conn:
        conn.execute(stmt)

for obs in observations:
    insert_obs(obs)

db = SQLDatabase(engine)
sql_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

sql_tool = Tool(
    name='Stock DB',
    func=sql_chain.run,
    description="Useful for when you need to answer questions about stocks " \
                "and their prices."
) 

tools = load_tools(
    ["llm-math"], 
    llm=llm
)
tools.append(sql_tool)

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
    st.title("Try SQL Langchain Agents 🦜")
    st.table(observations)
    form = st.form('AgentsTools')
    question = form.text_input("Enter your question", "")
    btn = form.form_submit_button("Run")

    if btn:
        st.markdown("### Response Agent AI")
        with st.spinner("Loading"):
            
            agent = initialize_agent(
                    agent="zero-shot-react-description", 
                    tools=tools, 
                    llm=llm,
                    verbose=True,
                    max_iterations=3,
                )            
            st.info(capture_and_display_output(agent.run, question))


if __name__ == "__main__":
    main()