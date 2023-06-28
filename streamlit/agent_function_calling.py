import openai
import streamlit as st
from streamlit_chat import message
import os
import json
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import whisper
from audiorecorder import audiorecorder

# cargamos openai api key
load_dotenv()

# Setting page title and header
st.set_page_config(page_title="Judini", page_icon=":robot_face:", layout="wide")
st.markdown("<h1 style='text-align: center;'>Talk with your data 🤖 <small>by <a href='https://judini.ai'>Judini</small></h1>", unsafe_allow_html=True)
audio = audiorecorder("Start recording", "Click to stop")

col1, col2 = st.columns(2)
# Datos de ejemplo para el inventario
data = {
    "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "items": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
    ],
    "cantidad": [5, 30, 10, 20, 40, 25, 12, 15, 50, 70],
    "detalles": [
        "Detalle A",
        "Detalle B",
        "Detalle C",
        "Detalle D",
        "Detalle E",
        "Detalle F",
        "Detalle G",
        "Detalle H",
        "Detalle I",
        "Detalle J",
    ], 
    "fecha": [ "2022-01-01", "2022-02-15", "2022-03-12", "2022-04-18", "2022-05-10", "2022-06-24", "2022-07-02", "2022-07-17", "2022-08-05", "2022-09-20", ]
}

df = pd.DataFrame(data)
new_df = pd.DataFrame({})
show_new_data = False

# function calling: orderBy df
def order_by(df, field, order):
    # orderBy
    if order == 'asc':
        order_boolean = True
    else:
        order_boolean = False
    
    df_ordenado = df.sort_values(by=field, ascending=order_boolean)
    show_new_data = True
    return df_ordenado

# function calling: create plot
def create_plot(tipo_grafico, titulo, campo_x, campo_y, df):
    fig = plt.figure()
    
    if tipo_grafico == 'bar':
        plt.bar(df[campo_x], df[campo_y])
    elif tipo_grafico == 'line':
        plt.plot(df[campo_x], df[campo_y])
    elif tipo_grafico == 'scatter':
        plt.scatter(df[campo_x], df[campo_y])
    else:
        raise ValueError("Tipo de gráfico no soportado")
    
    plt.xlabel(campo_x)
    plt.ylabel(campo_y)
    plt.title(titulo)
    st.pyplot(fig)


# whisper
model = whisper.load_model('base')

# UI
if len(audio) > 0:
        # To play audio in frontend:
        st.audio(audio.tobytes())
        
        # To save audio to a file:
        wav_file = open("audio.mp3", "wb")
        wav_file.write(audio.tobytes())

        # Whisper
        output = model.transcribe("audio.mp3")
        with st.spinner('Wait for it...'):
            user_audio = output['text']
            if len(user_audio) > 0:
                st.write('User: ', user_audio)
                openai.organization = os.getenv("ORG_ID")
                openai.api_key = os.getenv("OPENAI_API_KEY")
                response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[
                    {"role": "user", "content": user_audio}],
                functions=[
                    {
                        "name": "order_by",
                        "description": "Order by data",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "field": {
                                    "type": "string",
                                    "description": "Field by which the table will be ordered"
                                },
                                "order": {
                                    "type": "string",
                                    "description": "Order type ascending or descending by which the table will be sorted, could by true or false"
                                }
                            },
                        },
                    }
                ],
                function_call="auto",
                )
            message = response["choices"][0]["message"]
            st.markdown("<hr>", unsafe_allow_html=True)
            st.write('Function Calling gpt-3.5-turbo-0613: ', message)

            if message.get("function_call"):
                function_name = message["function_call"]["name"]
                #st.write('function_name: ', function_name)

                if(function_name == 'order_by'):
                    # Access the arguments
                    arguments = json.loads(message['function_call']['arguments'])
                    field_arg = arguments['field']
                    order_arg = arguments['order']
                    show_new_data = True
                    new_df = order_by(df, field_arg, order_arg)


# boton_ordenar = st.button("Ordenar por 'campo' descendente")
# if boton_ordenar:
#     df = order_by(df, 'cantidad', 'asc')
# Contenido de la columna izquierda
col1.header("Datos actuales")
col1.write(df)

col2.header("New Data")
if show_new_data:
    col2.write(new_df)
#st.header("Gráfico de barras de la cantidad de items")
#create_plot("bar", "Cantidad de artículos del inventario", "items", "cantidad", df)
