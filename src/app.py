import streamlit as st
import google.generativeai as genai
from services.classificacao import classificar_perfil

#  Configuração da API do Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
modelo = genai.GenerativeModel('gemini-2.5-flash')

st.title("SamFinance 💰")

st.write("Vamos analisar sua situação financeira!")

renda = st.number_input("Renda mensal", min_value=0.0)
gastos_fixos = st.number_input("Gastos fixos", min_value=0.0)
gastos_variaveis = st.number_input("Gastos variáveis", min_value=0.0)
dividas = st.number_input("Dívidas", min_value=0.0)

possui_veiculo = st.checkbox("Possui veículo?")
moradia = st.selectbox("Moradia", ["Alugada", "Própria"])

# Analisar perfil e gerar orientação
if st.button("Analisar"):
    usuario = {
        "renda": renda,
        "gastos_fixos": gastos_fixos,
        "gastos_variaveis": gastos_variaveis,
        "dividas": dividas,
        "possui_veiculo": possui_veiculo,
        "moradia": moradia.lower()
    }

    perfil = classificar_perfil(usuario)
    
    contexto_prompt = f"""
    Você é o SamFinance, um consultor financeiro iniciante, educativo e acolhedor.
    Aja de acordo com sua persona.
    
    Dados do Usuário:
    - Renda: R$ {renda}
    - Possui Veículo: {'Sim' if possui_veiculo else 'Não'}
    - Moradia: {moradia}
    
    Classificação do sistema: {perfil}
    
    Gere uma resposta curta e amigável aconselhando esse usuário com base na classificação.
    """
    
    st.success(f"Seu perfil calculado é: {perfil}")
    
    # Chamando a IA
    with st.spinner("SamFinance está analisando..."):
        resposta = modelo.generate_content(contexto_prompt)
        
    st.info("Orientação do SamFinance:")
    st.write(resposta.text)
    
    st.write("---")
    
    # Cálculos matemáticos
    sobra = renda - (gastos_fixos + gastos_variaveis)
    st.write(f"Sobra mensal: R$ {sobra:.2f}")

    if renda > 0:
        percentual = ((gastos_fixos + gastos_variaveis) / renda) * 100
        st.write(f"Você compromete {percentual:.1f}% da sua renda")