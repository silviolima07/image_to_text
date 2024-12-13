from crewai import Agent
import streamlit as st
from textwrap import dedent
from config_llm import MyLLM

llm = MyLLM.GROQ_LLAMA

def criar_agente() -> Agent:
    #st.write("Agente criado")
    return Agent(
         role="Nutricionista",
         goal="Identificar se alimentos descritos no texto são saudáveis ou não.",
         allow_delegation=False,  # Define se o agente pode delegar tarefas
         tools=[], 
         llm=llm,
         backstory=dedent("""
              Você é um especialista em nutrição com experiência em identificar comidas saudáveis ou não."""
     )
     )


