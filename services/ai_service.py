"""Integração com a API da OpenAI para avaliação semântica de respostas."""
import json
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

_client: OpenAI | None = None

SYSTEM_PROMPT = """Você é um avaliador semântico de respostas para um mini-game de enigmas em português.

Sua função é comparar a resposta do usuário com a resposta correta do enigma, levando em conta:
- Sinônimos e palavras equivalentes (ex: "relógio" = "cronômetro")
- Variações de acentuação e capitalização
- Singular e plural (ex: "ave" = "aves")
- Variações regionais do português
- Frases descritivas que correspondam ao conceito correto

Retorne EXCLUSIVAMENTE um JSON válido (sem markdown, sem código, sem texto extra):
{"correta": true/false, "feedback": "mensagem motivacional curta em português, máximo 2 frases"}

Se correta=true: celebre e parabenize o jogador.
Se correta=false: encoraje sem revelar a resposta."""


def avaliar_resposta(
    descricao_enigma: str,
    resposta_correta: str,
    resposta_usuario: str,
) -> dict:
    """
    Chama a OpenAI para validar semanticamente a resposta do usuário.
    Retorna dict com chaves 'correta' (bool) e 'feedback' (str).
    """
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)

    user_content = f"""Enigma: {descricao_enigma}
Resposta correta: {resposta_correta}
Resposta do usuário: {resposta_usuario}"""

    try:
        completion = _client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
            max_tokens=150,
            response_format={"type": "json_object"},
        )
        raw = completion.choices[0].message.content or "{}"
        result = json.loads(raw)
        return {
            "correta": bool(result.get("correta", False)),
            "feedback": result.get("feedback", "Não consegui avaliar. Tente novamente."),
        }
    except Exception as e:
        # Fallback: comparação simples por texto em caso de falha da API
        correta = resposta_usuario.strip().lower() == resposta_correta.strip().lower()
        return {
            "correta": correta,
            "feedback": "✅ Correto!" if correta else "❌ Resposta incorreta. Tente novamente!",
            "erro": str(e),
        }
