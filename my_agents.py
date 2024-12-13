from crewai import Agent
import streamlit as st
from textwrap import dedent
from config_llm import MyLLM

llm = MyLLM.GROQ_LLAMA

st.write("LLM do agente:", llm)

def criar_agente() -> Agent:
    #st.write("Agente criado")
    return Agent(
         role="Nutricionista",
         goal="Identificar se alimentos na descrição  são saudáveis ou não.",
         allow_delegation=False,  # Define se o agente pode delegar tarefas
         tools=[], 
         verbose=True,
         llm=llm,
         backstory=dedent("""
              Você é um especialista em nutrição com experiência em identificar comidas saudáveis ou não."""
     )
     )
    
