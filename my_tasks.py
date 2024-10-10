from crewai import Task
import streamlit as st

#
    
def criar_task(agente1):
    #st.write("Criando a task")
    analise = Task(
        name='analise_imagem',
        description= """
        Analise as palavras chaves na questão: {question}.
        Mostrar a palavra 'image2text' e descrever a imagem baseada na questão {question} e na imagem: {image}
        """,
        expected_output="Arquivo {descricao},  tipo markdown, um texto claro, em Português do Brasil.",
        
        agent=agente1,
        output_file="descricao_img.md",
        llm="groq/llava-v1.5-7b-4096-preview",
        provider='groq'
    )    
    st.write("Task: criada com sucesso")
    return analise

def executar_task(analise, image):
    st.write(image) 
    mensagem = {
         "role": "user",
         "content": f"Analise a seguinte imagem: {image}"
     }
    
    try:
        resultado = analise.execute(mensagem)
        return resultado
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

   
