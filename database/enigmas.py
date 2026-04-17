"""Operações CRUD para a tabela `enigmas`."""
from database.supabase_client import get_client


def listar_enigmas(dificuldade: str | None = None, apenas_ativos: bool = True) -> list[dict]:
    client = get_client()
    query = client.table("enigmas").select("*")
    if apenas_ativos:
        query = query.eq("ativo", True)
    if dificuldade:
        query = query.eq("dificuldade", dificuldade)
    res = query.order("dificuldade").execute()
    return res.data or []


def buscar_enigma(enigma_id: str) -> dict | None:
    client = get_client()
    res = client.table("enigmas").select("*").eq("id", enigma_id).execute()
    return res.data[0] if res.data else None


def enigmas_nao_resolvidos_pelo_usuario(usuario_id: str) -> list[dict]:
    """Retorna enigmas ativos que o usuário ainda não venceu."""
    client = get_client()
    # IDs dos enigmas já vencidos
    vencidos = (
        client.table("rodadas")
        .select("enigma_id")
        .eq("usuario_id", usuario_id)
        .eq("status", "vitoria")
        .execute()
    )
    ids_vencidos = [r["enigma_id"] for r in (vencidos.data or [])]

    todos = listar_enigmas(apenas_ativos=True)
    return [e for e in todos if e["id"] not in ids_vencidos]


def criar_enigma(
    titulo: str,
    descricao: str,
    resposta_correta: str,
    dificuldade: str,
    dica_1: str = "",
    dica_2: str = "",
    dica_3: str = "",
) -> dict | None:
    from config import PONTUACAO_INICIAL

    client = get_client()
    res = (
        client.table("enigmas")
        .insert(
            {
                "titulo": titulo,
                "descricao": descricao,
                "resposta_correta": resposta_correta,
                "dica_1": dica_1,
                "dica_2": dica_2,
                "dica_3": dica_3,
                "dificuldade": dificuldade,
                "pontuacao_inicial": PONTUACAO_INICIAL[dificuldade],
                "ativo": True,
            }
        )
        .execute()
    )
    return res.data[0] if res.data else None


def alternar_ativo(enigma_id: str, ativo: bool) -> None:
    client = get_client()
    client.table("enigmas").update({"ativo": ativo}).eq("id", enigma_id).execute()
