from crewai import Task
import streamlit as st
from textwrap import dedent
#
    
def criar_task(agente1):
    #st.write("Criando a task")
    analise = Task(
        name='analise_imagem',
        description= dedent("""
        Análise os alimentos na descrição: {descricao}.
        Informar o que é saudável ou não.
        """),
        expected_output=dedent(
        """
             Texto claro, em Português do Brasil.         
             Um relatório detalhado com:            
             1 - Alimentos identificados na descrição;
             2 - Identificar as vitaminas presentes em cada alimento;
             3 - Informar se alimento é saudável ou não;
             4-  Informar as calorias de cada alimento;
             5 - Informar qual beneficio o alimento oferece para a saúde;
             6 - Informar alternativa mais saudável para trocar pelo alimento.
             7 - Um resumo final do conjunto de alimentos descritos no texto.
             
             Exemplo a ser seguido:
             Ao analisar os alimentos descritos na imagem, podemos identificar os seguintes alimentos saudáveis:

* Tomates: ricos em vitamina C e lycopene, um antioxidante que ajuda a prevenir doenças crônicas.
* Salada com alface, tomate e cebola: a alface é rica em fibras e vitamina A, enquanto os tomates e a cebola fornecem vitamina C e flavonoides, respectivamente.
* Feijão: rico em fibras, proteínas e minerais como o ferro, o zinco e o magnésio.

Já os alimentos que podem ser considerados menos saudáveis ou que devem ser consumidos em moderação são:

* Carne (steak): embora seja uma boa fonte de proteínas, a carne vermelha consumida em excesso pode contribuir para o aumento do risco de doenças cardíacas e câncer. Além disso, a gordura presente na carne pode ser alta em calorias e gorduras saturadas.
* Batatas: embora sejam uma boa fonte de carboidratos, as batatas cozidas podem ter um alto índice glicêmico, o que pode ser problemático para pessoas com diabetes ou que desejam controlar o peso.
* Arroz: embora seja uma boa fonte de carboidratos, o arroz branco refinado pode ser pobre em fibras e nutrientes essenciais.

Em resumo, a imagem apresenta uma refeição equilibrada e saudável, 
com uma balança adequada entre proteínas, carboidratos e vegetais. 
No entanto, é importante ter cuidado com a quantidade de carne e 
batatas consumidas e optar por opções mais saudáveis, como 
arroz integral e feijão cozido.
             
              """),
        
        agent=agente1,
        provider='groq'
    )    
    #st.write("Task: criada com sucesso")
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

   
