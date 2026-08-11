import streamlit as st
from groq import Groq
import PyPDF2 # Nova ferramenta para ler PDFs!

# 1. DESIGN DO SITE (Fica mais largo e moderno)
st.set_page_config(page_title="Luna AI", page_icon="🌙", layout="wide")

# Conectando com o cofre de segurança
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. CRIANDO A MEMÓRIA DA LUNA
if "mensagens" not in st.session_state:
    # Se a conversa acabou de começar, dá a personalidade pra ela
    st.session_state.mensagens = [
        {"role": "system", "content": "Você é a Luna AI, uma assistente virtual inteligente. Ajude o usuário com tarefas, resumos e estudos. Responda sempre em português do Brasil e use emojis amigáveis."}
    ]

# 3. MENU LATERAL (Sidebar bonita)
with st.sidebar:
    st.title("🌙 Luna AI")
    st.write("Sua assistente pessoal de tarefas.")
    st.divider() # Linha de separação
    
    st.subheader("📎 Enviar Arquivos")
    arquivo_up = st.file_uploader("Envie um PDF ou Texto aqui:", type=["pdf", "txt"])
    
    st.divider()
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.mensagens = [st.session_state.mensagens[0]]
        st.rerun()

# 4. TELA PRINCIPAL DE CHAT (Estilo WhatsApp)
st.title("💬 Conversa")

# Mostra todas as mensagens antigas na tela
for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 5. CAIXA DE TEXTO LÁ EMBAIXO
pergunta = st.chat_input("Digite sua mensagem para a Luna...")

if pergunta:
    # Mostra a pergunta do usuário na tela
    with st.chat_message("user"):
        st.markdown(pergunta)

    # 6. LEITURA DE ARQUIVO (A mágica!)
    texto_arquivo = ""
    if arquivo_up is not None:
        if arquivo_up.name.endswith(".txt"):
            texto_arquivo = arquivo_up.getvalue().decode("utf-8")
        elif arquivo_up.name.endswith(".pdf"):
            leitor_pdf = PyPDF2.PdfReader(arquivo_up)
            for pagina in leitor_pdf.pages:
                texto_arquivo += pagina.extract_text() + "\n"
        
        texto_arquivo = f"\n\n[O USUÁRIO ENVIOU ESTE ARQUIVO PARA VOCÊ LER:\n{texto_arquivo}]"

    # Salva a pergunta (junto com o texto do arquivo, se tiver) na memória
    st.session_state.mensagens.append({"role": "user", "content": pergunta + texto_arquivo})

    # 7. RESPOSTA DA LUNA
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Luna está digitando... ✍️")
        
        # Manda TODA A MEMÓRIA para o Groq
        resposta = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.mensagens
        )
        
        texto_resposta = resposta.choices[0].message.content
        placeholder.markdown(texto_resposta)
    
    # Salva a resposta na memória
    st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})