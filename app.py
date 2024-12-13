import pandas as pd
import streamlit as st
from crewai import Crew, Process
from my_agents import criar_agente

from my_tasks import criar_task
from my_tools import save_uploaded_pdf, read_txt
from config_llm import llama_groq, llava_groq
import pdfplumber
import os
from PIL import Image
import time
from dotenv import load_dotenv
from groq import Groq
import chardet

import base64

from textwrap import dedent

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')  


# def image_to_text(client, model, b64_image, prompt):
    # # Criando a string que inclui o prompt e a imagem em base64
    # content_string = f"{prompt}\n\nImagem base64: data:image/png;base64,{b64_image}"
    
    # result = client.chat.completions.create(
    # messages=[
        # {
            # "role": "user",
            # "content": [
                # {"type": "text", "text": prompt},
                # {
                    # "type": "image_url",
                    # "image_url": {
                        # "url": f"data:image/png;base64,{b64_image}",
                    # },
                # },
            # ],
       # }
    # ],
    # model=model
    # )
  
    # return result.choices[0].message.content  
    
def image_to_text(client, model, b64_image, prompt):
    
    result = client.chat.completions.create(
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            #{
             #   "role": "system",
    #"content": f""" You are an expert assistant in recognizing and describing images with precision. 
    #Your role is to analyze images and provide clear, detailed, and accurate descriptions, considering both visual and contextual elements.
    #When you receive an image, you should offer a detailed and precise description of all visible elements.
    #"""
    #        #},
            {
                "role": "user",
                "content": [
                {'type': 'text', 'text': prompt},
                {
                  'type': 'image_url',
                  'image_url': {
                                 'url':f"data:image/jpeg;base64,{b64_image}",
                    }, 
                },
              ], 
            }    
        ], 
        model=model,
        temperature=0.5,  # Controla a criatividade
        top_p=0.9,  # Controla a diversidade das respostas
   )      
  
    return result.choices[0].message.content
    
def selecionar_idioma():
    st.markdown("#### Output in:")
    idioma = st.radio(
    "Output in:",
    ["Portuguese", "English"],
    horizontal = True,
    label_visibility='collapsed'
    )
    return idioma   
 
#def image_to_text2(client, model, b64_image, prompt):
    # Reduza o prompt para algo mais curto
#    prompt = "Analise a imagem fornecida."

    # Passar a string combinando o prompt e a imagem base64
#    content_string = f"{prompt}\n\nImagem base64: data:image/png;base64,{b64_image}"

#    result = client.chat.completions.create(
#        messages=[
#            {
#                "role": "user",
#                "content": content_string  # Garantindo que o conteúdo seja o menor possível
#            }
#        ],
#        model=model
#    )
  
#    return result.choices[0].message.content
 
        
# Função para executar a crew
def executar_crew(crew, inputs):
    try:
        result = crew.kickoff(inputs=inputs)  # Inicia a execução da crew
        return result  # Obtém a saída após a execução
    except Exception as e:
        st.error(f"Ocorreu um erro ao executar a crew: {e}")

# Função para configurar a crew com a task
def configurar_crew(agent, task, base64_image):
    # Mensagem a ser enviada
    mensagem = {
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
            },
        ],
    }

    inputs = {
               'idioma': idioma,
               'mensagem': mensagem
               }
               
    # Criar um Crew e adicionar a Task
    crew = Crew(agent=agent)
    crew.add_task(task, inputs=inputs)  # Adiciona a task e a mensagem

    return crew
    
# Carregar variáveis de ambiente
load_dotenv()

# Obter a chave da API GROQ
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
st.write("Groq key:", GROQ_API_KEY)

from groq import Groq

client_groq = Groq()
completion = client_groq.chat.completions.create(
    model="llama-3.2-90b-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "descreva esa imagem"
                },
            ]
        },
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

st.write(completion.choices[0].message)

   
   
