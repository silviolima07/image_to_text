import pandas as pd
import streamlit as st
from crewai import Crew, Process
from my_agents import criar_agente

from my_tasks import criar_task
from config_llm import MyLLM, llama_groq_mm

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
    
#def image_to_text(client, model, b64_image, prompt, idioma):
def image_to_text(client, model, b64_image, prompt):
    #language_instruction = {
    #"Portuguese": ("Responda em português com descrições precisas e detalhadas dos alimentos. "
    #               "Use frases claras e bem estruturadas."),
    #"English": "Respond in English with precise and detailed descriptions of the food. Use clear and structured sentences."
#}
    # Adiciona a instrução de idioma ao prompt
    #prompt = f"{prompt}\n\n{language_instruction[idioma]}"
  
    result = client.chat.completions.create(
        messages=[
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
        
# Função para executar a crew
def executar_crew(crew, inputs):
    try:
        result = crew.kickoff(inputs=inputs)  # Inicia a execução da crew
        st.write("Result from analyse of description")
        st.write(result)
      
        return result  # Obtém a saída após a execução
    except Exception as e:
        st.error(f"Ocorreu um erro ao executar a crew: {e}")

    
# Carregar variáveis de ambiente
load_dotenv()

# Obter a chave da API GROQ
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)
    
llama = MyLLM.GROQ_LLAMA.model
llama = llama_groq_mm # describe imgs

html_page_title = """
<div style="background-color:black;padding=60px">
        <p style='text-align:center;font-size:60px;font-weight:bold; color:red'>Descrição de Alimentos em Imagens</p>
</div>
"""               
st.markdown(html_page_title, unsafe_allow_html=True)

garfo_colher = Image.open("img/garfo_colher2.png")
st.sidebar.image(garfo_colher,caption="",use_column_width=True)

st.sidebar.markdown("# Menu")
option = st.sidebar.selectbox("Menu", ["Image", 'About'], label_visibility='hidden')

if option == 'Image':
    st.markdown("#### Objetivo: informar se é saudável ou não.")
    
    try:
        st.markdown("## Upload Image")
        uploaded_img = st.file_uploader("Envie imagem em PNG/JPG", type=['png', 'jpeg'])
        if uploaded_img is not None:
            img = Image.open(uploaded_img) # Load the image
            image_path="image.png"
            img.save(image_path)
            # Getting the base64 string
            base64_image = encode_image(image_path)
            # Usando HTML para centralizar a imagem
            st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{base64_image}" alt="Imagem" style="width: 80%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )
            
            prompt = dedent("""         
    You are an expert assistant in recognizing and describing foods in images with precision.
    
    Your role is to analyze images and provide description of foods, giving details, like color,size and accurate descriptions of foods.

    Always considering only foods present in the image.
    
    Never describe cars, trucks,  places in image, focus on foods only.
    
    If the image contains no food, respond only with the phrase: 'None food in image.'
    
    
}
    """)
            
            # Configuração da crew com o agente recrutador
            agente_nutri = criar_agente()
            #st.write("Objetivo: "+agente_nutri.goal)
            # Cria a task usando o agente criado
            #st.write('Criar a task')
            task_analise = criar_task(agente_nutri)
            #st.write(task_analise)
            st.write(" ")
            st.markdown("## Analisar Imagem")
            idioma = selecionar_idioma()
            
            #st.info("#### Avalie sempre a resposta final. O agente tem razão ou não?")
            
            
            crew = Crew(
                  agents=[agente_nutri],
                  tasks=[task_analise],
                  process=Process.sequential,  # Processamento sequencial das tarefas
                  verbose=True
                 
               )
          
            st.markdown("##### LLM MULTI MODAL: "+llama)
            llm = MyLLM.GROQ_LLAMA.model
            st.write("LLM do agente:", llm)
          
            if st.button("INICIAR"):
              
                with st.spinner('Wait for it...we are working...please'):
                    # Executa o CrewAI
                  
                    try:
                         
                        #descricao = image_to_text(client, llama, base64_image, prompt, idioma)
                        descricao = image_to_text(client, llama, base64_image, prompt)
                        # Exibindo a descricao
                        st.write("Descrição da imagem:")
                        
                        st.write(descricao)
                        
                        inputs = {
                      'descricao': descricao,
                      'idioma': idioma}
            
                        # Executando a crew
                        answer = "None food in image"
                        if descricao.lower() != answer.lower():
                            st.markdown("### Analysing if health or not")
                            resultado = executar_crew(crew, inputs)
                            #result_text = resultado.raw
                            st.write("Analise: ")
                            st.write(resultado)
                            # Exibindo o texto com um tamanho de fonte maior
                            # Substituindo quebras de linha por <br> e aplicando o estilo a todo o texto
                            #st.markdown(f"<div style='font-size:23px'>{result_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("### "+descricao)
                        
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao executar a crew: {e}")
        
        else:
            st.markdown("##### Formato PNG/JPEG")        
    except:
        st.error("Houston, we have a problem.")
if option == 'About':
    prato = Image.open("img/prato.png")
    st.sidebar.image(prato,caption="",use_column_width=True)
    st.markdown("### A partir da descrição da imagem feita por um agente especialista, usando o modelo llama,  um agente nutricionista, com modelo llama, informa se alimento é saudável.")
    st.markdown("### Modelos acessados via Groq.")
    st.markdown("### Exemplo:")
    st.write("""
    Ao analisar os alimentos descritos na imagem, podemos identificar os seguintes alimentos saudáveis:

* Salada com alface, tomate e cenoura: a alface é rica em fibras e vitamina A, enquanto os tomates fornecem vitamina C e lycopene, e as cenouras são ricas em vitamina A e fibras.
* Tomates: ricos em vitamina C e lycopene, um antioxidante que ajuda a prevenir doenças crônicas.
* Cenouras: são ricas em vitamina A e fibras, importante para a saúde dos olhos e do sistema imunológico.

Já os alimentos que podem ser considerados menos saudáveis ou que devem ser consumidos em moderação são:

* Carne (beef e sausage): embora sejam boas fontes de proteínas, a carne vermelha consumida em excesso pode contribuir para o aumento do risco de doenças cardíacas e câncer. Além disso, a gordura presente na carne pode ser alta em calorias e gorduras saturadas. O consumo exagerado de sausage também pode levar ao consumo excessivo de sódio e preservantes.
* Arroz: embora seja uma boa fonte de carboidratos, o arroz branco refinado pode ser pobre em fibras e nutrientes essenciais. É importante optar por opções mais saudáveis, como arroz integral.
Em resumo, a imagem apresenta uma refeição equilibrada, com uma balança adequada entre proteínas, 
carboidratos e vegetais. No entanto, é importante ter cuidado com a quantidade de carne e arroz 
consumidos e optar por opções mais saudáveis. Além disso, a adição de salsa ao prato pode ser benéfica, 
pois fornece vitamina C e flavonoides..""")    
   
