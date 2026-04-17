"""Página de seleção de enigma."""
import streamlit as st
from database import enigmas as db_enigmas


DIFICULDADE_LABEL = {"facil": "🟢 Fácil", "medio": "🟡 Médio", "dificil": "🔴 Difícil"}
DIFICULDADE_PONTOS = {"facil": "5.000 pts", "medio": "10.000 pts", "dificil": "15.000 pts"}


def render():
    usuario = st.session_state.get("usuario", {})
    st.markdown(
        f"""
        <div class="page-header">
            <h2>🧩 Escolha seu Enigma</h2>
            <p>Olá, <strong>{usuario.get('username', 'Jogador')}</strong>!
               Pontuação total: <strong>{usuario.get('pontuacao_total', 0):,}</strong> pts</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pendentes = db_enigmas.enigmas_nao_resolvidos_pelo_usuario(usuario["id"])

    if not pendentes:
        st.markdown(
            """
            <div class="victory-banner">
                🏆 Parabéns! Você resolveu TODOS os enigmas!<br>Confira seu ranking abaixo.
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🏅 Ver Ranking", use_container_width=True):
            st.session_state["pagina"] = "ranking"
            st.rerun()
        return

    # Filtro por dificuldade
    filtro = st.selectbox(
        "Filtrar por dificuldade",
        ["Todos", "🟢 Fácil", "🟡 Médio", "🔴 Difícil"],
        key="filtro_dificuldade",
    )
    mapa_filtro = {"Todos": None, "🟢 Fácil": "facil", "🟡 Médio": "medio", "🔴 Difícil": "dificil"}
    diff_selecionada = mapa_filtro[filtro]
    if diff_selecionada:
        pendentes = [e for e in pendentes if e["dificuldade"] == diff_selecionada]

    if not pendentes:
        st.info("Nenhum enigma disponível para este filtro.")
        return

    st.markdown(f"**{len(pendentes)} enigma(s) disponível(is)**")
    st.markdown("---")

    cols = st.columns(2)
    for i, enigma in enumerate(pendentes):
        with cols[i % 2]:
            dif = enigma["dificuldade"]
            st.markdown(
                f"""
                <div class="enigma-card">
                    <div class="enigma-card-badge {dif}">{DIFICULDADE_LABEL[dif]}</div>
                    <h4>{enigma['titulo']}</h4>
                    <p class="enigma-preview">{enigma['descricao'][:80]}…</p>
                    <p class="enigma-points">💰 {DIFICULDADE_PONTOS[dif]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Jogar →", key=f"jogar_{enigma['id']}", use_container_width=True):
                st.session_state["enigma_selecionado"] = enigma
                st.session_state["rodada"] = None
                st.session_state["pagina"] = "jogo"
                st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏅 Ranking", use_container_width=True):
            st.session_state["pagina"] = "ranking"
            st.rerun()
    with col2:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()
