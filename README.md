# Enigma Quest 🧩

Mini-game de enigmas com validação semântica por IA.

## Stack

| Camada | Tecnologia |
|---|---|
| Frontend | Streamlit |
| Banco de dados | Supabase (PostgreSQL) |
| IA | OpenAI API (gpt-4o-mini) |

## Setup

### 1. Clone o repositório

```bash
git clone <repo-url>
cd mini-game-enigma-uj
```

### 2. Crie o ambiente virtual e instale dependências

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

Valores necessários no `.env`:
- `SUPABASE_URL` — URL do seu projeto no Supabase
- `SUPABASE_ANON_KEY` — Chave anon do Supabase
- `OPENAI_API_KEY` — Sua chave da OpenAI

### 4. Configure o banco de dados

No [painel do Supabase](https://app.supabase.com):
1. Vá em **SQL Editor**
2. Cole e execute o conteúdo de `sql/schema.sql`

Isso criará as tabelas `usuarios`, `enigmas`, `rodadas` e `tentativas`, além de popular o banco com 8 enigmas de exemplo.

### 5. Rode a aplicação

```bash
streamlit run app.py
```

Acesse em: http://localhost:8501

---

## Estrutura do Projeto

```
mini-game-enigma-uj/
├── app.py              # Entry point + CSS dark theme + roteamento
├── config.py           # Configurações e constantes do jogo
├── requirements.txt
├── .env.example
├── database/
│   ├── supabase_client.py
│   ├── usuarios.py
│   ├── enigmas.py
│   ├── rodadas.py
│   └── tentativas.py
├── services/
│   ├── ai_service.py   # Validação semântica via OpenAI
│   └── game_engine.py  # Motor de regras
├── pages/
│   ├── login.py
│   ├── selecao.py
│   ├── game.py
│   ├── ranking.py
│   └── admin.py        # Acesse via st.session_state["pagina"] = "admin"
└── sql/
    └── schema.sql
```

## Regras do Jogo

| Dificuldade | Pontuação Inicial |
|---|---|
| 🟢 Fácil | 5.000 pts |
| 🟡 Médio | 10.000 pts |
| 🔴 Difícil | 15.000 pts |

**Penalidades:**
- Resposta errada: -1.000 pts
- Dica 1: -1.000 pts | Dica 2: -2.000 pts | Dica 3: -3.000 pts
- Derrota: pontuação ≤ 0
- Vitória: pontos restantes somados ao ranking global

## Acessar Administração

Na sessão ativa, execute no console Python ou adicione botão na interface:
```python
st.session_state["pagina"] = "admin"
```
Ou acesse diretamente via URL adicionando `?admin=true` e ajustando o roteamento.
