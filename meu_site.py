import streamlit as st
from groq import Groq

# ⬇️ COLE A SUA CHAVE DO GROQ (que começa com gsk_) AQUI DENTRO DAS ASPAS ⬇️
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Design do site
st.set_page_config(page_title="Luna AI", page_icon="🌙")
st.title("🌙 Luna AI")
st.write("Olá! Eu sou a Luna, sua assistente virtual. Como posso te ajudar hoje?")

pergunta_do_usuario = st.text_input("Digite sua pergunta para a Luna:")

if st.button("Enviar"):
    if pergunta_do_usuario == "":
        st.warning("Por favor, digite uma pergunta primeiro!")
    else:
        with st.spinner('A Luna está pensando na velocidade da luz...'):
            # Mandando a pergunta pro cérebro do Groq
            resposta = client.chat.completions.create(
                model="llama-3.1-8b-instant", # Este é o cérebro super rápido que vamos usar
                messages=[
                    {"role": "system", "content": "Você se chama Luna AI. Você é uma inteligência artificial amigável, inteligente e muito prestativa. Fale português do Brasil."},
                    {"role": "user", "content": pergunta_do_usuario}
                ]
            )
            
            texto_resposta = resposta.choices[0].message.content
            st.success("Luna AI diz:")
            st.write(texto_resposta)