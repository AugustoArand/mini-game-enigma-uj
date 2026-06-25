"""
Enigma Quest — Entry point do Streamlit.
Gerencia session state e roteamento entre páginas.
"""
import streamlit as st

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Enigma Quest",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS Global (Minimal Dark Theme) ────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ── Tokens ── */
    :root {
        --bg:          #0c0c10;
        --surface:     #13131a;
        --surface-2:   #1a1a25;
        --border:      #252535;
        --border-soft: #1e1e2e;
        --accent:      #6d5ce7;
        --accent-soft: #2d2850;
        --accent-dim:  #4a40a0;
        --text-1:      #e8e8f0;
        --text-2:      #9090aa;
        --text-3:      #5a5a72;
        --green:       #3ecf8e;
        --green-bg:    #0e2a1e;
        --green-border:#1a4a32;
        --yellow:      #f5c842;
        --yellow-bg:   #2a2010;
        --yellow-border:#4a3a10;
        --red:         #e05555;
        --red-bg:      #2a1010;
        --red-border:  #4a1a1a;
        --radius:      10px;
        --radius-lg:   16px;
    }

    /* ── Reset & Base ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    .stApp {
        background-color: var(--bg);
        min-height: 100vh;
    }
    .block-container {
        max-width: 780px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* ── Auth Header ── */
    .auth-header {
        text-align: center;
        padding: 3.5rem 0 2.5rem;
    }
    .auth-logo {
        width: 56px;
        height: 56px;
        border-radius: 14px;
        background: var(--accent-soft);
        border: 1px solid var(--accent-dim);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.25rem;
    }
    .auth-logo svg {
        width: 28px;
        height: 28px;
        fill: none;
        stroke: #a08cf5;
        stroke-width: 1.5;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    .auth-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: var(--text-1);
        letter-spacing: -0.02em;
        margin: 0;
    }
    .auth-header p {
        color: var(--text-2);
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.4rem;
        letter-spacing: 0.01em;
    }

    /* ── Page Header ── */
    .page-header {
        padding: 1.25rem 0 1.25rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }
    .page-header h2 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: var(--text-1);
        margin: 0;
        letter-spacing: -0.01em;
    }
    .page-header p {
        color: var(--text-2);
        margin: 0.25rem 0 0;
        font-size: 0.9rem;
    }
    .page-header .user-pill {
        display: inline-block;
        background: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.2rem 0.75rem;
        font-size: 0.8rem;
        color: var(--text-2);
        margin-top: 0.5rem;
    }
    .page-header .user-pill strong { color: var(--text-1); font-weight: 500; }

    /* ── Enigma Cards (Seleção) ── */
    .enigma-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.1rem 1.2rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .enigma-card:hover {
        border-color: var(--accent-dim);
        box-shadow: 0 4px 24px rgba(109,92,231,0.12);
    }
    .enigma-card h4 {
        color: var(--text-1);
        margin: 0.5rem 0 0.3rem;
        font-size: 0.95rem;
        font-weight: 600;
    }
    .enigma-preview { color: var(--text-2); font-size: 0.82rem; margin: 0; line-height: 1.5; }
    .enigma-points {
        color: var(--accent);
        font-weight: 600;
        font-size: 0.82rem;
        margin: 0.5rem 0 0;
        letter-spacing: 0.01em;
    }
    .enigma-card-badge { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }

    /* ── Game Header ── */
    .game-header {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.25rem;
    }
    .game-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-1);
        margin-bottom: 0.75rem;
    }
    .score-display { display: flex; flex-direction: column; gap: 0.3rem; }
    .score-label { font-size: 0.72rem; color: var(--text-3); letter-spacing: 0.05em; text-transform: uppercase; font-weight: 500; }
    .score-value { color: var(--accent); font-size: 1.3rem; font-weight: 700; font-family: 'Space Grotesk', sans-serif; }
    .score-bar-bg {
        background: var(--border);
        border-radius: 999px;
        height: 4px;
        overflow: hidden;
        margin-top: 0.3rem;
    }
    .score-bar {
        height: 100%;
        border-radius: 999px;
        transition: width 0.5s ease, background 0.5s ease;
    }

    /* ── Badge dificuldade ── */
    .badge { padding: 0.2rem 0.65rem; border-radius: 999px; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; }
    .badge.facil   { background: var(--green-bg);   color: var(--green);  border: 1px solid var(--green-border); }
    .badge.medio   { background: var(--yellow-bg);  color: var(--yellow); border: 1px solid var(--yellow-border); }
    .badge.dificil { background: var(--red-bg);     color: var(--red);    border: 1px solid var(--red-border); }

    /* ── Enigma Box ── */
    .enigma-box {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: 0 var(--radius) var(--radius) 0;
        padding: 1.4rem 1.75rem;
        margin: 1rem 0 1.5rem;
    }
    .enigma-text {
        color: var(--text-1);
        font-size: 1.1rem;
        font-style: italic;
        line-height: 1.75;
        margin: 0;
        font-weight: 300;
    }

    /* ── Section labels ── */
    .section-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-3);
        margin: 1.25rem 0 0.75rem;
    }

    /* ── Feedback entries ── */
    .feedback-entry {
        border-radius: var(--radius);
        padding: 0.75rem 1rem;
        margin: 0.35rem 0;
        font-size: 0.88rem;
        line-height: 1.55;
    }
    .feedback-entry.correct { background: var(--green-bg); border: 1px solid var(--green-border); color: #6de0ab; }
    .feedback-entry.wrong   { background: var(--red-bg);   border: 1px solid var(--red-border);   color: #e08888; }
    .feedback-entry .answer-label { font-weight: 600; color: inherit; opacity: 0.9; }
    .feedback-entry .status-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-right: 0.4rem;
        vertical-align: middle;
    }
    .feedback-entry.correct .status-dot { background: var(--green); }
    .feedback-entry.wrong   .status-dot { background: var(--red); }

    /* ── Result banners ── */
    .result-banner {
        text-align: center;
        border-radius: var(--radius-lg);
        padding: 2rem;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0;
        line-height: 1.6;
    }
    .result-banner.vitoria {
        background: var(--green-bg);
        border: 1px solid var(--green-border);
        color: var(--green);
    }
    .result-banner.derrota {
        background: var(--red-bg);
        border: 1px solid var(--red-border);
        color: var(--red);
    }
    .result-points { font-size: 0.9rem; font-weight: 400; display: block; margin-top: 0.5rem; opacity: 0.8; }

    /* ── Victory banner (seleção) ── */
    .victory-banner {
        background: var(--surface);
        border: 1px solid var(--border);
        border-top: 3px solid var(--accent);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.15rem;
        color: var(--text-1);
        margin: 1rem 0;
    }
    .victory-banner p { color: var(--text-2); font-size: 0.9rem; margin-top: 0.4rem; font-family: 'Inter', sans-serif; }

    /* ── Ranking Table ── */
    .ranking-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .ranking-table th {
        background: var(--surface);
        color: var(--text-3);
        padding: 0.75rem 1rem;
        text-align: left;
        font-weight: 500;
        font-size: 0.72rem;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        border-bottom: 1px solid var(--border);
    }
    .ranking-table td {
        padding: 0.7rem 1rem;
        border-bottom: 1px solid var(--border-soft);
        color: var(--text-1);
        font-size: 0.9rem;
    }
    .ranking-table tr:hover td { background: var(--surface); }
    .ranking-table tr.ranking-me td {
        background: var(--accent-soft);
        color: #b0a0f8;
        font-weight: 500;
    }
    .rank-pos { color: var(--text-3); font-variant-numeric: tabular-nums; font-weight: 600; }
    .rank-pos.top1 { color: #f5c842; }
    .rank-pos.top2 { color: #b0b8c8; }
    .rank-pos.top3 { color: #c08060; }

    /* ── Streamlit overrides ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-1) !important;
        border-radius: var(--radius) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(109,92,231,0.18) !important;
    }
    .stButton > button {
        background: var(--surface-2) !important;
        color: var(--text-1) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.01em !important;
        transition: background 0.15s ease, border-color 0.15s ease !important;
        padding: 0.5rem 1.25rem !important;
    }
    .stButton > button:hover {
        background: var(--accent-soft) !important;
        border-color: var(--accent-dim) !important;
        color: #c4b8f8 !important;
    }
    /* Primary-style button (first in each block) */
    .stButton:first-child > button {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
        color: #fff !important;
    }
    .stButton:first-child > button:hover {
        background: var(--accent-dim) !important;
        border-color: var(--accent-dim) !important;
        color: #fff !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid var(--border) !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        color: var(--text-2) !important;
        padding: 0.5rem 1.2rem !important;
        border-radius: 0 !important;
        border-bottom: 2px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text-1) !important;
        border-bottom-color: var(--accent) !important;
        background: transparent !important;
    }
    .stSelectbox > div > div {
        background: var(--surface) !important;
        border-color: var(--border) !important;
        color: var(--text-1) !important;
        border-radius: var(--radius) !important;
    }
    div[data-testid="stExpander"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
    }
    div[data-testid="stExpander"]:hover {
        border-color: var(--border) !important;
    }
    label { color: var(--text-2) !important; font-size: 0.85rem !important; font-weight: 400 !important; }
    h3 { color: var(--text-1) !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 1.1rem !important; font-weight: 600 !important; }
    h4 { color: var(--text-1) !important; font-size: 0.95rem !important; }
    hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
    .stInfo { background: #0e1e2e !important; border: 1px solid #1a3550 !important; color: #88b8e0 !important; border-radius: var(--radius) !important; }
    .stError { background: var(--red-bg) !important; border: 1px solid var(--red-border) !important; border-radius: var(--radius) !important; }
    .stSuccess { background: var(--green-bg) !important; border: 1px solid var(--green-border) !important; border-radius: var(--radius) !important; }
    .stWarning { background: var(--yellow-bg) !important; border: 1px solid var(--yellow-border) !important; border-radius: var(--radius) !important; }
    p { color: var(--text-2); font-size: 0.9rem; line-height: 1.6; }
    strong { color: var(--text-1) !important; font-weight: 500 !important; }
    /* Hide Streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }
    /* Spinner */
    .stSpinner > div { border-top-color: var(--accent) !important; }
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
