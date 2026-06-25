"""Página de Login e Registro."""
import streamlit as st
from database import usuarios as db_usuarios


def render():
    st.markdown(
        """
        <div class="auth-header">
            <div class="auth-logo">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                    <path d="M2 17l10 5 10-5"/>
                    <path d="M2 12l10 5 10-5"/>
                </svg>
            </div>
            <h1>Enigma Quest</h1>
            <p>Desafie sua mente. Prove sua inteligência.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_login, tab_registro = st.tabs(["Entrar", "Criar conta"])

    with tab_login:
        _form_login()

    with tab_registro:
        _form_registro()


def _form_login():
    with st.form("form_login", clear_on_submit=False):
        st.markdown("### Acesse sua conta")
        email = st.text_input("E-mail", placeholder="seu@email.com", key="login_email")
        senha = st.text_input("Senha", type="password", placeholder="••••••••", key="login_senha")
        submitted = st.form_submit_button("Entrar", use_container_width=True)

    if submitted:
        if not email or not senha:
            st.error("Preencha e-mail e senha.")
            return
        try:
            usuario = db_usuarios.autenticar(email, senha)
            if usuario:
                st.session_state["usuario"] = usuario
                st.session_state["pagina"] = "selecao"
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")
        except Exception as e:
            st.error(f"Erro ao conectar com o banco: {e}")


def _form_registro():
    with st.form("form_registro", clear_on_submit=True):
        st.markdown("### Crie sua conta")
        username = st.text_input("Nome de usuário", placeholder="ex: HeroDosEnigmas", key="reg_username")
        email = st.text_input("E-mail", placeholder="seu@email.com", key="reg_email")
        senha = st.text_input("Senha", type="password", placeholder="••••••••", key="reg_senha")
        senha2 = st.text_input("Confirmar senha", type="password", placeholder="••••••••", key="reg_senha2")
        submitted = st.form_submit_button("Criar conta", use_container_width=True)

    if submitted:
        if not all([username, email, senha, senha2]):
            st.error("Preencha todos os campos.")
            return
        if senha != senha2:
            st.error("As senhas não coincidem.")
            return
        if len(senha) < 6:
            st.error("A senha deve ter pelo menos 6 caracteres.")
            return
        try:
            usuario = db_usuarios.criar_usuario(username, email, senha)
            if usuario:
                st.session_state["usuario"] = usuario
                st.session_state["pagina"] = "selecao"
                st.success("Conta criada! Bem-vindo ao Enigma Quest.")
                st.rerun()
            else:
                st.error("Erro inesperado: nenhum dado retornado. Tente novamente.")
        except Exception as e:
            erro = str(e)
            if "unique" in erro.lower() or "duplicate" in erro.lower():
                st.error("Este e-mail ou username já está em uso.")
            else:
                st.error(f"Erro ao criar conta: {erro}")
