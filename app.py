"""
Enigma Quest — Entry point do Streamlit.
Gerencia session state e roteamento entre páginas.
"""
import streamlit as st

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Enigma Quest",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS Global (Dark Theme) ─────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;900&display=swap');

    /* ── Reset & Base ── */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0d0d1a 0%, #111827 50%, #0d0d1a 100%);
        min-height: 100vh;
    }
    .block-container {
        max-width: 800px;
        padding-top: 2rem;
    }

    /* ── Auth Header ── */
    .auth-header {
        text-align: center;
        padding: 3rem 0 2rem;
    }
    .auth-header .logo-icon {
        font-size: 4rem;
        display: block;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 20px #7c3aed);
    }
    .auth-header h1 {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #7c3aed, #a78bfa, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .auth-header p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* ── Page Header ── */
    .page-header {
        text-align: center;
        padding: 1.5rem 0 1rem;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 1.5rem;
    }
    .page-header h2 {
        font-size: 2rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 0;
    }
    .page-header p {
        color: #94a3b8;
        margin: 0.3rem 0 0;
    }

    /* ── Enigma Cards (Seleção) ── */
    .enigma-card {
        background: linear-gradient(145deg, #1e1b4b, #1e293b);
        border: 1px solid #312e81;
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .enigma-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(124,58,237,0.25);
    }
    .enigma-card h4 {
        color: #e2e8f0;
        margin: 0.5rem 0 0.3rem;
        font-size: 1rem;
        font-weight: 600;
    }
    .enigma-preview { color: #94a3b8; font-size: 0.85rem; margin: 0; }
    .enigma-points { color: #a78bfa; font-weight: 600; font-size: 0.9rem; margin: 0.4rem 0 0; }
    .enigma-card-badge { font-size: 0.75rem; font-weight: 600; }

    /* ── Game Header ── */
    .game-header {
        background: linear-gradient(145deg, #1e1b4b, #0f172a);
        border: 1px solid #312e81;
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .game-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.8rem;
    }
    .score-display { display: flex; flex-direction: column; gap: 0.3rem; }
    .score-value { color: #a78bfa; font-size: 1.4rem; font-weight: 700; }
    .score-bar-bg {
        background: #1e293b;
        border-radius: 999px;
        height: 8px;
        overflow: hidden;
    }
    .score-bar {
        height: 100%;
        border-radius: 999px;
        transition: width 0.5s ease, background 0.5s ease;
    }

    /* ── Badge dificuldade ── */
    .badge { padding: 0.2rem 0.7rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }
    .badge.facil  { background: #14532d; color: #4ade80; }
    .badge.medio  { background: #713f12; color: #facc15; }
    .badge.dificil { background: #7f1d1d; color: #f87171; }

    /* ── Enigma Box ── */
    .enigma-box {
        background: linear-gradient(145deg, #0f172a, #1e1b4b);
        border-left: 4px solid #7c3aed;
        border-radius: 0 12px 12px 0;
        padding: 1.5rem 2rem;
        margin: 1rem 0 1.5rem;
    }
    .enigma-text {
        color: #e2e8f0;
        font-size: 1.2rem;
        font-style: italic;
        line-height: 1.7;
        margin: 0;
    }

    /* ── Feedback entries ── */
    .feedback-entry {
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    .feedback-entry.correct { background: #14532d33; border: 1px solid #16a34a; color: #86efac; }
    .feedback-entry.wrong   { background: #7f1d1d33; border: 1px solid #dc2626; color: #fca5a5; }

    /* ── Result banners ── */
    .result-banner {
        text-align: center;
        border-radius: 16px;
        padding: 2rem;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 1.5rem 0;
        line-height: 1.6;
    }
    .result-banner.vitoria {
        background: linear-gradient(135deg, #14532d, #166534);
        border: 2px solid #16a34a;
        color: #86efac;
    }
    .result-banner.derrota {
        background: linear-gradient(135deg, #7f1d1d, #991b1b);
        border: 2px solid #dc2626;
        color: #fca5a5;
    }
    .result-points { font-size: 1rem; font-weight: 400; display: block; margin-top: 0.5rem; }

    /* ── Victory banner (seleção) ── */
    .victory-banner {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border: 2px solid #7c3aed;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        font-size: 1.3rem;
        color: #c4b5fd;
        margin: 1rem 0;
    }

    /* ── Ranking Table ── */
    .ranking-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .ranking-table th {
        background: #1e1b4b;
        color: #a78bfa;
        padding: 0.8rem 1rem;
        text-align: left;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .ranking-table td {
        padding: 0.7rem 1rem;
        border-bottom: 1px solid #1e293b;
        color: #e2e8f0;
        font-size: 0.95rem;
    }
    .ranking-table tr:hover td { background: #1e293b55; }
    .ranking-table tr.ranking-me td {
        background: #312e8144;
        color: #c4b5fd;
        font-weight: 600;
    }

    /* ── Streamlit overrides ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124,58,237,0.3) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: opacity 0.2s !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
    }
    .stSelectbox > div > div {
        background: #1e293b !important;
        border-color: #334155 !important;
        color: #e2e8f0 !important;
    }
    div[data-testid="stExpander"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    label { color: #94a3b8 !important; }
    h3, h4 { color: #e2e8f0 !important; }
    hr { border-color: #1e293b !important; }
    .stInfo { background: #1e3a5f33 !important; border-color: #38bdf8 !important; }
    .stError { background: #7f1d1d33 !important; border-color: #dc2626 !important; }
    .stSuccess { background: #14532d33 !important; border-color: #16a34a !important; }
    .stWarning { background: #713f1233 !important; border-color: #ca8a04 !important; }
    /* Hide Streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Roteamento ──────────────────────────────────────────────────────────────
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

pagina = st.session_state["pagina"]
usuario_logado = st.session_state.get("usuario")

# Redireciona para login se não autenticado
if not usuario_logado and pagina != "login":
    pagina = "login"
    st.session_state["pagina"] = "login"

# ── Renderização ────────────────────────────────────────────────────────────
if pagina == "login":
    from pages import login
    login.render()

elif pagina == "selecao":
    from pages import selecao
    selecao.render()

elif pagina == "jogo":
    from pages import game
    game.render()

elif pagina == "ranking":
    from pages import ranking
    ranking.render()

elif pagina == "admin":
    from pages import admin
    admin.render()
