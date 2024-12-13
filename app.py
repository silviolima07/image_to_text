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

print(completion.choices[0].message)


client = Groq()

st.write("Client groq:", client)
"""
# Criando o checkbox para mostrar ou não os comandos das tasks
#mostrar_comandos = st.checkbox("Mostrar progresso das tarefas em execução", value=True)

# Função para mostrar o progresso da execução das tarefas e capturar o resultado final
#def executar_tarefas(crew, inputs):
#    st.write("### Executando as tasks...")

    # Variável para armazenar o resultado final após a execução de todas as tasks
#    result = None

    # Executa as tasks uma por uma e exibe o progresso no Streamlit
#    for i, task in enumerate(crew.tasks):
#        task_agent = (task.agent.role) # Nome do agente responsavel, definido em my_agents
#        task_name = (task.name).upper()  # Nome da tasks, definido tem my_tasks
#        st.write(f"Agent : **{task_agent}**")  # Mostra o nome do agent
#        st.write(f"Executando task : **{task_name}**")  # Mostra o nome da task
#        st.write(f"Descrição:")
#        st.write(f"{task.description}")
#        time.sleep(2)  # Simula o tempo de execução da task
        # Aqui você pode simular o progresso de cada task, ou capturar a execução real

    # Após a execução de todas as tasks, salva o resultado
#    result = crew.kickoff(inputs=inputs)
    
#    return result  # Retorna o resultado final


# Função para ler o PDF e extrair o texto
#def extract_text_from_pdf(uploaded_file):
#    text_content = ""
#    with pdfplumber.open(uploaded_file) as pdf:
#        for page in pdf.pages:
#            text_content += page.extract_text() + "\n"
#    return text_content

# Função para salvar o conteúdo extraído em um arquivo txt
#def save_to_txt(text_content, output_filename="profile.txt"):
#    with open(output_filename, "w", encoding="latin1") as text_file:
#        text_file.write(text_content)

# Função para ler o conteúdo de um arquivo markdown
#def read_markdown_file(file_path):
#    if os.path.exists(file_path):
#        with open(file_path, "r", encoding="utf-8") as file:
#            return file.read()
#    else:
#        raise FileNotFoundError(f"Arquivo {file_path} não encontrado.")

#def executar_task(analise, image):
#     mensagem = {
#         "role": "user",
#         "content": f"Analise a seguinte imagem: {image}"
#     }
#    
#     try:
#         resultado = analise.invoke(mensagem)
#         return resultado
#     except Exception as e:
#         st.error(f"Ocorreu um erro: {e}")



# Função para redimensionar a imagem e convertê-la para Base64
def resize_image(image_path, max_width=200):
    img = Image.open(image_path)
    st.write("Image process...")
    
    # Redimensiona a imagem mantendo a proporção
    #st.write('Width:',img.width, 'Max:',200)
    if img.width > max_width:
        
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        st.write("- resized")
        

    # Converte a imagem redimensionada para Base64
    #buffer = io.BytesIO()
    #img.save(buffer, format="PNG")
    #img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    image_path="image.png"
    img.save(image_path)
    img_base64 = encode_image(image_path)
    st.write("- converted to base64")
    st.image(img)
    
    return img_base64
    
llama = llama_groq
llava = llava_groq
    

# Configuração da crew com o agente recrutador
agente_nutri = criar_agente(llama)
#st.write("Objetivo: "+agente_nutri.goal)
# Cria a task usando o agente criado
#st.write('Criar a task')
task_analise = criar_task(agente_nutri)


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
    """)
            
            # Configuração da crew com o agente recrutador
            #agente_nutri = criar_agente(llama)
            #st.write("Objetivo: "+agente_nutri.goal)
            # Cria a task usando o agente criado
            #st.write('Criar a task')
            #task_analise = criar_task(agente_nutri)
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
            #st.write(crew)
            #st.markdown("#### "+prompt)

            if st.button("INICIAR"):
                #inputs = {
                #      'question': "Fornecer uma descrição detalhada da imagem",
                #      'image': base64_image,
                #      'descricao': 'descricao_img.md'}
                      
                with st.spinner('Wait for it...we are working...please'):
                    # Executa o CrewAI
                    
                    
                    try:
                    
                            
                        descricao = image_to_text(client, llava, base64_image, prompt)
                        # Exibindo a descricao
                        #st.write("Descrição da imagem:")
                        
                        #st.write(descricao)
                        
                        inputs = {
                      'descricao': descricao,
                      'idioma': idioma}
            
                        #result = crew.kickoff(inputs=inputs)
                        #st.write(result)
                        #executar_tarefas(crew)
                        #executar_task(task_analise, base64_image)
                        
                        # Criando a task
                        #task = criar_task(agent)

                        # Configurando a crew com a task
                        #crew = configurar_crew(agente1, task_analise, base64_image)

                        # Executando a crew
                        answer = "None food in image"
                        if descricao.lower() != answer.lower():
                            
                            resultado = executar_crew(crew, inputs)
                            result_text = resultado.raw
                            #st.write(resultado)
                            #st.write(result_text)
                            # Exibindo o texto com um tamanho de fonte maior
                            # Substituindo quebras de linha por <br> e aplicando o estilo a todo o texto
                            st.markdown(f"<div style='font-size:23px'>{result_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
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
    st.markdown("### A partir da descrição da imagem feita por um agente especialista, usando o modelo llava,  um agente nutricionista, com modelo llama, informa se alimento é saudável.")
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
   
