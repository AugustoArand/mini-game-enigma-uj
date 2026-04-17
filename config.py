import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY: str = os.environ["SUPABASE_ANON_KEY"]
OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Motor de regras
PONTUACAO_INICIAL = {
    "facil": 5000,
    "medio": 10000,
    "dificil": 15000,
}

PENALIDADE_RESPOSTA_ERRADA = 1000
PENALIDADE_DICA = {1: 1000, 2: 2000, 3: 3000}
