"""Página principal do jogo — enigma ativo."""
import streamlit as st
from services.game_engine import processar_tentativa, usar_dica, iniciar_nova_rodada
from database import rodadas as db_rodadas


DIFICULDADE_LABEL = {"facil": "🟢 Fácil", "medio": "🟡 Médio", "dificil": "🔴 Difícil"}


def render():
    enigma = st.session_state.get("enigma_selecionado")
    usuario = st.session_state.get("usuario")

    if not enigma or not usuario:
        st.session_state["pagina"] = "selecao"
        st.rerun()

    # Inicializar rodada se não existir
    if not st.session_state.get("rodada"):
        rodada = iniciar_nova_rodada(usuario["id"], enigma)
        st.session_state["rodada"] = rodada
        st.session_state["dicas_reveladas"] = []
        st.session_state["historico_feedback"] = []
    else:
        rodada = st.session_state["rodada"]

    # Recarregar rodada do banco para ter dados atualizados
    rodada = db_rodadas.buscar_rodada(rodada["id"])
    if not rodada:
        st.error("Erro ao carregar a rodada.")
        return

    _render_header(enigma, rodada)

    status = rodada["status"]

    if status == "vitoria":
        _render_vitoria(rodada, enigma)
        return
    if status == "derrota":
        _render_derrota(rodada, enigma)
        return

    _render_enigma(enigma)
    _render_dicas(rodada, enigma)
    _render_tentativa(rodada, enigma)
    _render_historico()


def _render_header(enigma: dict, rodada: dict):
    pontuacao = rodada["pontuacao_atual"]
    pontuacao_inicial = enigma["pontuacao_inicial"]
    pct = max(0, pontuacao / pontuacao_inicial)
    dif = enigma["dificuldade"]

    cor_barra = "#4ade80" if pct > 0.6 else "#facc15" if pct > 0.3 else "#f87171"

    st.markdown(
        f"""
        <div class="game-header">
            <div class="game-title">
                <span>{enigma['titulo']}</span>
                <span class="badge {dif}">{DIFICULDADE_LABEL[dif]}</span>
            </div>
            <div class="score-display">
                <span class="score-value">💰 {pontuacao:,} pts</span>
                <div class="score-bar-bg">
                    <div class="score-bar" style="width:{pct*100:.0f}%; background:{cor_barra};"></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_enigma(enigma: dict):
    st.markdown(
        f"""
        <div class="enigma-box">
            <p class="enigma-text">"{enigma['descricao']}"</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_dicas(rodada: dict, enigma: dict):
    dicas_usadas: int = rodada["dicas_usadas"]
    from config import PENALIDADE_DICA

    st.markdown("#### 💡 Dicas")
    dicas_reveladas = st.session_state.get("dicas_reveladas", [])

    for n, texto in enumerate(dicas_reveladas, 1):
        st.info(f"**Dica {n}:** {texto}")

    if dicas_usadas < 3:
        proxima = dicas_usadas + 1
        custo = PENALIDADE_DICA[proxima]
        if st.button(
            f"🔍 Revelar Dica {proxima} (-{custo:,} pts)",
            key=f"dica_{proxima}",
            use_container_width=True,
        ):
            resultado = usar_dica(rodada, enigma)
            st.session_state["dicas_reveladas"].append(resultado["texto_dica"])
            # Atualizar rodada no session_state
            rodada_atualizada = db_rodadas.buscar_rodada(rodada["id"])
            st.session_state["rodada"] = rodada_atualizada
            if resultado["pontuacao_atual"] <= 0:
                st.rerun()
            st.rerun()
    else:
        st.caption("Todas as dicas foram reveladas.")


def _render_tentativa(rodada: dict, enigma: dict):
    st.markdown("#### 🎯 Sua Resposta")
    with st.form("form_tentativa", clear_on_submit=True):
        resposta = st.text_input(
            "Digite sua resposta",
            placeholder="Ex: relógio...",
            key="campo_resposta",
        )
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("✅ Confirmar Resposta", use_container_width=True)
        with col2:
            if st.form_submit_button("🏳 Desistir", use_container_width=True):
                from database import rodadas as db_r
                db_r.finalizar_rodada(rodada["id"], "derrota")
                st.session_state["rodada"] = db_r.buscar_rodada(rodada["id"])
                st.rerun()

    if submitted:
        if not resposta.strip():
            st.warning("Digite uma resposta antes de confirmar.")
            return

        with st.spinner("🤖 A IA está avaliando sua resposta..."):
            resultado = processar_tentativa(rodada, enigma, resposta.strip())

        feedback_entry = {
            "resposta": resposta.strip(),
            "feedback": resultado.feedback,
            "correta": resultado.correta,
        }
        st.session_state.setdefault("historico_feedback", []).insert(0, feedback_entry)
        st.session_state["rodada"] = db_rodadas.buscar_rodada(rodada["id"])
        st.rerun()


def _render_historico():
    historico = st.session_state.get("historico_feedback", [])
    if not historico:
        return
    st.markdown("#### 📜 Histórico de Tentativas")
    for entry in historico:
        icon = "✅" if entry["correta"] else "❌"
        st.markdown(
            f"""
            <div class="feedback-entry {'correct' if entry['correta'] else 'wrong'}">
                {icon} <strong>"{entry['resposta']}"</strong><br>
                <em>{entry['feedback']}</em>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_vitoria(rodada: dict, enigma: dict):
    st.balloons()
    st.markdown(
        f"""
        <div class="result-banner vitoria">
            🏆 PARABÉNS! Você acertou!<br>
            <span class="result-points">+{rodada['pontuacao_atual']:,} pts adicionados ao seu ranking!</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Próximo Enigma", use_container_width=True):
            st.session_state["rodada"] = None
            st.session_state["dicas_reveladas"] = []
            st.session_state["historico_feedback"] = []
            st.session_state["pagina"] = "selecao"
            st.rerun()
    with col2:
        if st.button("🏅 Ver Ranking", use_container_width=True):
            st.session_state["pagina"] = "ranking"
            st.rerun()


def _render_derrota(rodada: dict, enigma: dict):
    st.markdown(
        f"""
        <div class="result-banner derrota">
            💀 Game Over! Seus pontos chegaram a zero.<br>
            <span class="result-points">A resposta era: <strong>{enigma['resposta_correta']}</strong></span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Tentar Novamente", use_container_width=True):
            st.session_state["rodada"] = None
            st.session_state["dicas_reveladas"] = []
            st.session_state["historico_feedback"] = []
            st.rerun()
    with col2:
        if st.button("🏠 Voltar à Seleção", use_container_width=True):
            st.session_state["rodada"] = None
            st.session_state["dicas_reveladas"] = []
            st.session_state["historico_feedback"] = []
            st.session_state["pagina"] = "selecao"
            st.rerun()
