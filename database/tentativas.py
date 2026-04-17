"""Operações CRUD para a tabela `tentativas`."""
from database.supabase_client import get_client


def registrar_tentativa(
    rodada_id: str,
    resposta_usuario: str,
    feedback_ia: str,
    correta: bool,
    penalidade_aplicada: int,
) -> dict | None:
    client = get_client()
    res = (
        client.table("tentativas")
        .insert(
            {
                "rodada_id": rodada_id,
                "resposta_usuario": resposta_usuario,
                "feedback_ia": feedback_ia,
                "correta": correta,
                "penalidade_aplicada": penalidade_aplicada,
            }
        )
        .execute()
    )
    return res.data[0] if res.data else None


def tentativas_da_rodada(rodada_id: str) -> list[dict]:
    client = get_client()
    res = (
        client.table("tentativas")
        .select("*")
        .eq("rodada_id", rodada_id)
        .order("created_at")
        .execute()
    )
    return res.data or []


def total_tentativas(rodada_id: str) -> int:
    tentativas = tentativas_da_rodada(rodada_id)
    return len(tentativas)
