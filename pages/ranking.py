"""Página de ranking global."""
import streamlit as st
from database import usuarios as db_usuarios


def render():
    st.markdown(
        """
        <div class="page-header">
            <h2>Ranking Global</h2>
            <p>Os maiores decifradores de enigmas</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top = db_usuarios.ranking(limite=20)
    usuario_atual = st.session_state.get("usuario", {})

    if not top:
        st.info("Nenhum jogador no ranking ainda. Seja o primeiro.")
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
            if i == 1:
                pos_cls = "rank-pos top1"
                pos_txt = "1"
            elif i == 2:
                pos_cls = "rank-pos top2"
                pos_txt = "2"
            elif i == 3:
                pos_cls = "rank-pos top3"
                pos_txt = "3"
            else:
                pos_cls = "rank-pos"
                pos_txt = str(i)

            destaque = "ranking-me" if row["username"] == usuario_atual.get("username") else ""
            pts = f"{row['pontuacao_total']:,}".replace(",", ".")
            st.markdown(
                f"""<tr class="{destaque}">
                    <td><span class="{pos_cls}">{pos_txt}</span></td>
                    <td>{row['username']}</td>
                    <td><strong>{pts}</strong> pts</td>
                </tr>""",
                unsafe_allow_html=True,
            )
        st.markdown("</tbody></table>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    if st.button("Voltar à seleção", use_container_width=True):
        st.session_state["pagina"] = "selecao"
        st.rerun()
