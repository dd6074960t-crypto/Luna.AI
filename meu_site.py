import streamlit as st
from groq import Groq
import PyPDF2
import urllib.parse # Ferramenta para criar links de imagens

# 1. DESIGN DO SITE
st.set_page_config(page_title="Luna AI", page_icon="🌙", layout="wide")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "system", "content": "Você é a Luna AI, uma assistente virtual inteligente. Ajude com tarefas, resumos e estudos. Fale em português do Brasil e use emojis."}
    ]

# 2. MENU LATERAL (Sidebar)
with st.sidebar:
    st.title("🌙 Luna AI")
    st.write("Sua assistente pessoal de tarefas.")
    st.divider()
    
    st.subheader("📎 Enviar Arquivos")
    arquivo_up = st.file_uploader("Envie um PDF ou Texto aqui:", type=["pdf", "txt"])
    
    st.divider()
    st.write("🎨 **DICA:** Para gerar imagens, digite `/imagem` antes do seu texto. Exemplo: `/imagem um gato de óculos escuros`")
    
    st.divider()
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.mensagens = [st.session_state.mensagens[0]]
        st.rerun()

# 3. TELA DE CHAT
st.title("💬 Conversa")

for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

pergunta = st.chat_input("Digite sua mensagem ou /imagem...")

if pergunta:
    # 4. VERIFICA SE O USUÁRIO QUER UMA IMAGEM
    if pergunta.lower().startswith("/imagem"):
        # Pega só o que o usuário digitou depois de "/imagem"
        descricao_imagem = pergunta.replace("/imagem", "").strip()
        
        # Transforma o texto em um link que o gerador de imagem entende
        texto_link = urllib.parse.quote(descricao_imagem)
        link_da_imagem = f"https://image.pollinations.ai/prompt/{texto_link}?nologo=true"
        
        # Mostra a pergunta
        with st.chat_message("user"):
            st.markdown(pergunta)
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        
        # A Luna responde com a imagem!
        resposta_luna = f"🎨 Aqui está a sua imagem de: **{descricao_imagem}**\n\n![Imagem gerada]({link_da_imagem})"
        with st.chat_message("assistant"):
            st.markdown(resposta_luna)
        st.session_state.mensagens.append({"role": "assistant", "content": resposta_luna})

    # 5. SE NÃO FOR IMAGEM, É CONVERSA NORMAL!
    else:
        with st.chat_message("user"):
            st.markdown(pergunta)

        texto_arquivo = ""
        if arquivo_up is not None:
            if arquivo_up.name.endswith(".txt"):
                texto_arquivo = arquivo_up.getvalue().decode("utf-8")
            elif arquivo_up.name.endswith(".pdf"):
                leitor_pdf = PyPDF2.PdfReader(arquivo_up)
                for pagina in leitor_pdf.pages:
                    texto_arquivo += pagina.extract_text() + "\n"
            texto_arquivo = f"\n\n[ARQUIVO PARA LER:\n{texto_arquivo}]"

        st.session_state.mensagens.append({"role": "user", "content": pergunta + texto_arquivo})

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Luna está digitando... ✍️")
            
            resposta = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.mensagens
            )
            
            texto_resposta = resposta.choices[0].message.content
            placeholder.markdown(texto_resposta)
        
        st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})