from crewai import Agent
import streamlit as st
from textwrap import dedent

def criar_agente(modelo) -> Agent:
    #st.write("Agente criado")
    return Agent(
         role="Nutricionista",
         goal="Identificar se alimentos descritos no texto são saudáveis ou não.",
         allow_delegation=False,  # Define se o agente pode delegar tarefas
         tools=[], 
         llm="groq/llama3-70b-8192", #llama,
         backstory=dedent("""
              Você é um especialista em nutrição com experiência em identificar comidas saudáveis ou não."""
     )
     )


