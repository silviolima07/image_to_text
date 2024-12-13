from crewai import Task
import streamlit as st
from textwrap import dedent
#
    
def criar_task(agente):
    st.write("Criando a task")
    analise = Task(
        name='analise_imagem',
        description= dedent("""
        Análise os alimentos na descrição: {descricao}.
        Informar o que é saudável ou não.
        """),
        expected_output=dedent(
        """
             Texto claro, em {idioma}.         
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

* Arroz: é uma boa fonte de carboidratos, mas é importante optar por arroz integral para garantir um conteúdo mais alto de fibras e nutrientes essenciais. O arroz integral é rico em fibras, vitamina B6 e magnésio. Cada xícara de arroz integral cozida fornece cerca de 216 calorias. O benefício para a saúde é que ajuda a controlar o nível de açúcar no sangue e a regular o trânsito intestinal. Alternativa mais saudável: não há necessidade de substituir, pois o arroz integral é uma opção saudável.

* Vegetais (legumes e verduras): são ricos em vitaminas, minerais e fibras. É provável que os vegetais incluídos sejam ricos em vitamina C, vitamina A, potássio e fibras. Cada xícara de vegetais cozidos fornece cerca de 50 calorias. O benefício para a saúde é que ajudam a prevenir doenças crônicas, como câncer e doenças cardíacas, e a regular o trânsito intestinal. Alternativa mais saudável: não há necessidade de substituir, pois os vegetais são uma opção saudável.

Já os alimentos que podem ser considerados menos saudáveis ou que devem ser consumidos em moderação são:

* Carne (meat): embora seja uma boa fonte de proteínas, a carne vermelha consumida em excesso pode contribuir para o aumento do risco de doenças cardíacas e câncer. Além disso, a gordura presente na carne pode ser alta em calorias e gorduras saturadas. Cada 100g de carne fornece cerca de 250 calorias. O benefício para a saúde é que fornece proteínas essenciais para o crescimento e desenvolvimento. Alternativa mais saudável: optar por cortes de carne mais magros ou por fontes de proteínas mais saudáveis, como peixe ou frango.

Em resumo, a imagem apresenta uma refeição equilibrada e saudável, com uma balança adequada entre proteínas, carboidratos e vegetais. No entanto, é importante ter cuidado com a quantidade de carne consumida e optar por opções mais saudáveis, como carne magra e vegetais cozidos.
             
              """),
        
        agent=agente
        #provider='groq'
    )    
    #st.write("Task: criada com sucesso")
    return analise

#def executar_task(analise, image):
#    st.write(image) 
#    mensagem = {
#         "role": "user",
#         "content": f"Analise a seguinte imagem: {image}"
#     }
    
#    try:
#        resultado = analise.execute(mensagem)
#        return resultado
#    except Exception as e:
#        st.error(f"Ocorreu um erro: {e}")

   
