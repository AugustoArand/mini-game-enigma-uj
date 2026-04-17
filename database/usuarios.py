"""Operações CRUD para a tabela `usuarios`."""
import hashlib
from database.supabase_client import get_client


def _hash(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def criar_usuario(username: str, email: str, senha: str) -> dict | None:
    """Cria um novo usuário. Retorna o registro ou levanta exceção em caso de erro."""
    client = get_client()
    res = (
        client.table("usuarios")
        .insert({"username": username, "email": email, "senha_hash": _hash(senha)})
        .execute()
    )
    return res.data[0] if res.data else None


def buscar_por_email(email: str) -> dict | None:
    client = get_client()
    res = client.table("usuarios").select("*").eq("email", email).execute()
    return res.data[0] if res.data else None


def buscar_por_username(username: str) -> dict | None:
    client = get_client()
    res = client.table("usuarios").select("*").eq("username", username).execute()
    return res.data[0] if res.data else None


def autenticar(email: str, senha: str) -> dict | None:
    """Retorna o usuário se credenciais baterem, None caso contrário."""
    usuario = buscar_por_email(email)
    if usuario and usuario["senha_hash"] == _hash(senha):
        return usuario
    return None


def atualizar_pontuacao(usuario_id: str, pontos_ganhos: int) -> dict | None:
    """Adiciona pontos_ganhos à pontuação total do usuário."""
    client = get_client()
    usuario = client.table("usuarios").select("pontuacao_total").eq("id", usuario_id).execute()
    if not usuario.data:
        return None
    nova_pontuacao = usuario.data[0]["pontuacao_total"] + pontos_ganhos
    res = (
        client.table("usuarios")
        .update({"pontuacao_total": nova_pontuacao})
        .eq("id", usuario_id)
        .execute()
    )
    return res.data[0] if res.data else None


def ranking(limite: int = 10) -> list[dict]:
    """Retorna o top N jogadores por pontuação total."""
    client = get_client()
    res = (
        client.table("usuarios")
        .select("username, pontuacao_total")
        .order("pontuacao_total", desc=True)
        .limit(limite)
        .execute()
    )
    return res.data or []
