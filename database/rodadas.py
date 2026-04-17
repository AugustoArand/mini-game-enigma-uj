"""Operações CRUD para a tabela `rodadas`."""
from database.supabase_client import get_client


def criar_rodada(usuario_id: str, enigma_id: str, pontuacao_inicial: int) -> dict | None:
    client = get_client()
    res = (
        client.table("rodadas")
        .insert(
            {
                "usuario_id": usuario_id,
                "enigma_id": enigma_id,
                "pontuacao_atual": pontuacao_inicial,
                "dicas_usadas": 0,
                "status": "em_andamento",
            }
        )
        .execute()
    )
    return res.data[0] if res.data else None


def buscar_rodada(rodada_id: str) -> dict | None:
    client = get_client()
    res = client.table("rodadas").select("*").eq("id", rodada_id).execute()
    return res.data[0] if res.data else None


def atualizar_pontuacao(rodada_id: str, nova_pontuacao: int) -> dict | None:
    client = get_client()
    res = (
        client.table("rodadas")
        .update({"pontuacao_atual": nova_pontuacao})
        .eq("id", rodada_id)
        .execute()
    )
    return res.data[0] if res.data else None


def incrementar_dica(rodada_id: str, dicas_usadas: int) -> dict | None:
    client = get_client()
    res = (
        client.table("rodadas")
        .update({"dicas_usadas": dicas_usadas + 1})
        .eq("id", rodada_id)
        .execute()
    )
    return res.data[0] if res.data else None


def finalizar_rodada(rodada_id: str, status: str) -> dict | None:
    """status: 'vitoria' | 'derrota'"""
    from datetime import datetime, timezone

    client = get_client()
    res = (
        client.table("rodadas")
        .update({"status": status, "finalizada_at": datetime.now(timezone.utc).isoformat()})
        .eq("id", rodada_id)
        .execute()
    )
    return res.data[0] if res.data else None


def rodadas_do_usuario(usuario_id: str) -> list[dict]:
    client = get_client()
    res = (
        client.table("rodadas")
        .select("*, enigmas(titulo, dificuldade)")
        .eq("usuario_id", usuario_id)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []
