import os
import openai
import streamlit as st

# Carrega a chave de API da variável de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configura a interface do Streamlit
st.set_page_config(page_title="💬 Chatbot Personalizado com IA", page_icon="💬", layout="centered")
st.title('💬 Chatbot Personalizado com IA')

# Inicializa a sessão de mensagens
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Função para exibir o histórico da conversa
def display_chat():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**Você:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Assistente:** {message['content']}")

# Função para processar a mensagem do usuário
def process_message(user_input):
    user_input = user_input.strip()
    if user_input:
        # Adiciona a mensagem do usuário à sessão
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Exibe o histórico da conversa atualizado
        display_chat()
        
        with st.spinner('Pensando...'):
            try:
                # Envia as mensagens para a API da OpenAI
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                # Obtém a resposta do assistente
                assistant_message = response['choices'][0]['message']['content']
                # Adiciona a resposta do assistente à sessão
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                # Exibe a resposta do assistente
                display_chat()
            except openai.error.AuthenticationError:
                st.error("Falha na autenticação. Verifique sua chave de API da OpenAI.")
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")

# Exibe o histórico da conversa
display_chat()

st.markdown("---")  # Linha horizontal para separar o chat do input

# Cria um formulário para entrada de mensagens com clear_on_submit=True
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Digite sua mensagem:", key='user_input')
    submit_button = st.form_submit_button(label='Enviar')

    if submit_button:
        process_message(user_input)

# Opcional: Botão para limpar o histórico da conversa
if st.button("🔄 Limpar Conversa"):
    st.session_state.messages = []
    st.experimental_rerun()
