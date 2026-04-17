import os
from dotenv import load_dotenv

load_dotenv()


def _get_secret(key: str, default: str | None = None) -> str:
    """
    Busca uma variável de configuração na seguinte ordem:
    1. st.secrets (Streamlit Cloud)
    2. os.environ / .env (desenvolvimento local)
    3. Levanta erro claro se não encontrada
    """
    # 1. Tenta st.secrets (disponível no Streamlit Cloud)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass

    # 2. Tenta variável de ambiente / .env
    value = os.environ.get(key, default)
    if value is not None:
        return value

    raise EnvironmentError(
        f"❌ Variável '{key}' não encontrada.\n"
        "Configure-a em:\n"
        "  • Streamlit Cloud: Manage App → Settings → Secrets\n"
        "  • Local: arquivo .env na raiz do projeto"
    )


SUPABASE_URL: str = _get_secret("SUPABASE_URL")
SUPABASE_ANON_KEY: str = _get_secret("SUPABASE_ANON_KEY")
OPENAI_API_KEY: str = _get_secret("OPENAI_API_KEY")
OPENAI_MODEL: str = _get_secret("OPENAI_MODEL", "gpt-4o-mini")

# Motor de regras
PONTUACAO_INICIAL = {
    "facil": 5000,
    "medio": 10000,
    "dificil": 15000,
}

PENALIDADE_RESPOSTA_ERRADA = 1000
PENALIDADE_DICA = {1: 1000, 2: 2000, 3: 3000}
