"""Página de administração — cadastro e gestão de enigmas."""
import streamlit as st
from database import enigmas as db_enigmas


DIFICULDADE_LABEL = {"facil": "Fácil", "medio": "Médio", "dificil": "Difícil"}


def render():
    st.markdown(
        """
        <div class="page-header">
            <h2>Administração</h2>
            <p>Gerencie os enigmas do jogo</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_novo, tab_listar = st.tabs(["Novo enigma", "Listar enigmas"])

    with tab_novo:
        _form_novo_enigma()

    with tab_listar:
        _listar_enigmas()

    st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button("Voltar à seleção", use_container_width=True):
        st.session_state["pagina"] = "selecao"
        st.rerun()


def _form_novo_enigma():
    with st.form("form_enigma", clear_on_submit=True):
        st.markdown("### Criar novo enigma")
        titulo = st.text_input("Título *", placeholder="Ex: O Guardião do Tempo")
        descricao = st.text_area("Enunciado *", placeholder="Descreva o enigma aqui...", height=100)
        resposta = st.text_input("Resposta correta *", placeholder="Ex: relógio")
        dificuldade = st.selectbox(
            "Dificuldade *",
            ["facil", "medio", "dificil"],
            format_func=lambda x: DIFICULDADE_LABEL[x],
        )
        st.markdown("**Dicas** _(opcionais)_")
        dica1 = st.text_input("Dica 1  ·  -1.000 pts")
        dica2 = st.text_input("Dica 2  ·  -2.000 pts")
        dica3 = st.text_input("Dica 3  ·  -3.000 pts")
        submitted = st.form_submit_button("Salvar enigma", use_container_width=True)

    if submitted:
        if not all([titulo, descricao, resposta]):
            st.error("Preencha os campos obrigatórios (*).")
            return
        enigma = db_enigmas.criar_enigma(titulo, descricao, resposta, dificuldade, dica1, dica2, dica3)
        if enigma:
            st.success(f"Enigma '{titulo}' criado com sucesso.")
        else:
            st.error("Erro ao criar enigma.")


def _listar_enigmas():
    todos = db_enigmas.listar_enigmas(apenas_ativos=False)
    if not todos:
        st.info("Nenhum enigma cadastrado.")
        return

    for e in todos:
        status_txt = "Ativo" if e["ativo"] else "Inativo"
        dif_txt = DIFICULDADE_LABEL.get(e["dificuldade"], e["dificuldade"])
        label = f"{dif_txt} — {e['titulo']}  ·  {status_txt}"
        with st.expander(label):
            st.markdown(f"**Enunciado:** {e['descricao']}")
            st.markdown(f"**Resposta:** `{e['resposta_correta']}`")
            pts = f"{e['pontuacao_inicial']:,}".replace(",", ".")
            st.markdown(f"**Pontuação inicial:** {pts} pts")
            if e.get("dica_1"):
                st.markdown(f"**Dica 1:** {e['dica_1']}")
            if e.get("dica_2"):
                st.markdown(f"**Dica 2:** {e['dica_2']}")
            if e.get("dica_3"):
                st.markdown(f"**Dica 3:** {e['dica_3']}")
            novo_ativo = not e["ativo"]
            label_btn = "Ativar" if novo_ativo else "Desativar"
            if st.button(label_btn, key=f"toggle_{e['id']}"):
                db_enigmas.alternar_ativo(e["id"], novo_ativo)
                st.rerun()
