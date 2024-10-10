# from crewai import Agent
# from crewai_tools import VisionTool
# #from app import modelo
# import streamlit as st

# vision_tool = VisionTool()

# Configuração do agente

# def criar_agente(modelo):
    
    # agente1 = Agent(
        # role="pesquisador",
        # goal="Ler o arquivo {profile}."
             # " Identificar imagem e texto.",
        # backstory=
            # "Você é um experiente pesquisador que sabe identificar imagens e textos."
        # ,
        # llm=modelo,
        # verbose=True,
        # memory=False,
        # tools=[vision_tool]
    # )
    # st.write("Agente1 criado")
    # return revisor_link  
    
from crewai import Agent
from crewai_tools import VisionTool  # Importe corretamente o VisionTool
import streamlit as st

# Inicialize a ferramenta VisionTool corretamente
vision_tool = VisionTool()

# Exemplo de como chamar a função passando a configuração
agents_config = {
    "researcher": {
        "role": "Pesquisador de Visão",
        "goal": "Utilizar ferramentas de visão para pesquisar imagens e informações visuais."
    }
}

def criar_agente(modelo) -> Agent:
    # agents_config = {
    # "researcher": {
        # "role": "Pesquisador de Visão",
        # "goal": "Enviar imagem para o modelo e descrever o que apresenta.",
        # 'llm':"groq/llava-v1.5-7b-4096-preview",
        # 'provider':'groq',
        # 'tools':[vision_tool],
        
                   # }
       # }
    st.write("Agent: criado com sucesso")
    
    # Cria e retorna o agente com o VisionTool
    return Agent(
         #config=agents_config["researcher"],  # Configuração do agente passada como argumento
         role="Pesquisador de Visão",
         goal="Enviar imagem para o modelo e descrever o que apresenta.",
         allow_delegation=False,  # Define se o agente pode delegar tarefas
         tools=[],        # Associa o VisionTool ao agente
         llm="groq/llava-v1.5-7b-4096-preview",
         backstory=
              "Você é um experiente pesquisador que sabe identificar imagens e textos."
     )



# Criação do agente pesquisador
#researcher_agent = criar_agente(modelo, agents_config)

