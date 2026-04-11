import streamlit as st
import google.generativeai as genai
from services.classificacao import classificar_perfil

# Configuração visual da página para ficar mais larga
st.set_page_config(page_title="SamFinance", page_icon="💰", layout="wide")

# Configuração da API usando a biblioteca clássica
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("SamFinance 💰")
st.write("Seu consultor financeiro inteligente.")


# BARRA LATERAL (CONFIGURAÇÃO INICIAL)

with st.sidebar:
    st.header("📋 Seu Perfil Financeiro")
    renda = st.number_input("Renda mensal", min_value=0.0)
    gastos_fixos = st.number_input("Gastos fixos", min_value=0.0)
    gastos_variaveis = st.number_input("Gastos variáveis", min_value=0.0)
    dividas = st.number_input("Dívidas", min_value=0.0)
    
    possui_veiculo = st.checkbox("Possui veículo?")
    moradia = st.selectbox("Moradia", ["Alugada", "Própria"])

    if st.button("Iniciar Consultoria"):
        usuario = {
            "renda": renda,
            "gastos_fixos": gastos_fixos,
            "gastos_variaveis": gastos_variaveis,
            "dividas": dividas,
            "possui_veiculo": possui_veiculo,
            "moradia": moradia.lower()
        }
        
        perfil = classificar_perfil(usuario)
        
        # Salva os dados na memória do Streamlit
        st.session_state["perfil"] = perfil
        st.session_state["mensagens"] = [] 
        
        # O System Prompt (A Personalidade)
        instrucao_sistema = """
        Você é o SamFinance, um consultor financeiro iniciante, educativo e acolhedor.
        Seu objetivo é ajudar pessoas a organizarem as finanças e montarem a primeira reserva.
        
        REGRAS:
        1. Baseie-se APENAS nos dados fornecidos na inicialização e na conversa.
        2. Seja amigável e acessível.
        3. Nunca faça recomendações diretas de investimento.
        4. Se o usuário possuir veículo, lembre-o dos gastos sazonais (IPVA, manutenção).
        5. Se a pessoa estiver "Endividada", seja encorajador e foque em corte de gastos e quitação.
        """
        
        # Cria o modelo passando as regras de comportamento
        modelo = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=instrucao_sistema
        )
        
        # Cria a SESSÃO DE CHAT clássica
        st.session_state["chat_session"] = modelo.start_chat(history=[])
        
        contexto_inicial = f"""
        Aja como SamFinance. Acabei de preencher meu perfil no sistema:
        - Renda: R$ {renda}
        - Gastos Totais: R$ {gastos_fixos + gastos_variaveis}
        - Dívidas: R$ {dividas}
        - Possui Veículo: {'Sim' if possui_veiculo else 'Não'}
        - Moradia: {moradia}
        - Classificação do sistema: {perfil}
        
        Faça uma breve e acolhedora análise inicial da minha situação para começarmos a conversar!
        """
        
        # A IA responde ao primeiro contexto
        response = st.session_state["chat_session"].send_message(contexto_inicial)
        
        # Salva a resposta no histórico (role model virou assistant para o ícone do streamlit)
        st.session_state["mensagens"].append({"role": "assistant", "text": response.text})


# TELA PRINCIPAL (INTERFACE DE CHAT)


# Se o chat já foi iniciado
if "chat_session" in st.session_state:
    st.success(f"Perfil Ativo: {st.session_state['perfil']}")
    
    # Desenha o histórico
    for msg in st.session_state["mensagens"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])
            
    # Campo de digitação
    if prompt := st.chat_input("Digite sua dúvida para o SamFinance..."):
        
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state["mensagens"].append({"role": "user", "text": prompt})
        
        with st.spinner("SamFinance digitando..."):
            resposta = st.session_state["chat_session"].send_message(prompt)
            
        with st.chat_message("assistant"):
            st.markdown(resposta.text)
        st.session_state["mensagens"].append({"role": "assistant", "text": resposta.text})

else:
    st.info("👈 Preencha seus dados na barra lateral e clique em 'Iniciar Consultoria' para começar a conversar com o SamFinance.")