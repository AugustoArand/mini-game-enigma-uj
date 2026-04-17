"""Página de ranking global."""
import streamlit as st
from database import usuarios as db_usuarios


MEDALS = ["🥇", "🥈", "🥉"]


def render():
    st.markdown(
        """
        <div class="page-header">
            <h2>🏆 Ranking Global</h2>
            <p>Os maiores decifradores de enigmas</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top = db_usuarios.ranking(limite=20)
    usuario_atual = st.session_state.get("usuario", {})

    if not top:
        st.info("Nenhum jogador no ranking ainda. Seja o primeiro!")
    else:
        st.markdown(
            """
            <table class="ranking-table">
                <thead>
                    <tr><th>#</th><th>Jogador</th><th>Pontuação</th></tr>
                </thead>
                <tbody>
            """,
            unsafe_allow_html=True,
        )
        for i, row in enumerate(top, 1):
            medal = MEDALS[i - 1] if i <= 3 else str(i)
            destaque = "ranking-me" if row["username"] == usuario_atual.get("username") else ""
            st.markdown(
                f"""<tr class="{destaque}">
                    <td>{medal}</td>
                    <td>{row['username']}</td>
                    <td><strong>{row['pontuacao_total']:,}</strong> pts</td>
                </tr>""",
                unsafe_allow_html=True,
            )
        st.markdown("</tbody></table>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🏠 Voltar à Seleção", use_container_width=True):
        st.session_state["pagina"] = "selecao"
        st.rerun()
