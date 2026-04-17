"""Motor de regras do jogo: aplica penalidades, avalia condições de vitória/derrota."""
from config import PENALIDADE_RESPOSTA_ERRADA, PENALIDADE_DICA
from database import rodadas as db_rodadas, tentativas as db_tentativas, usuarios as db_usuarios
from services.ai_service import avaliar_resposta


class ResultadoTentativa:
    def __init__(
        self,
        correta: bool,
        feedback: str,
        pontuacao_atual: int,
        penalidade: int,
        status_rodada: str,
    ):
        self.correta = correta
        self.feedback = feedback
        self.pontuacao_atual = pontuacao_atual
        self.penalidade = penalidade
        self.status_rodada = status_rodada  # 'em_andamento' | 'vitoria' | 'derrota'


def processar_tentativa(
    rodada: dict,
    enigma: dict,
    resposta_usuario: str,
) -> ResultadoTentativa:
    """
    Avalia a resposta via IA, aplica penalidades e atualiza o banco.
    """
    avaliacao = avaliar_resposta(
        descricao_enigma=enigma["descricao"],
        resposta_correta=enigma["resposta_correta"],
        resposta_usuario=resposta_usuario,
    )

    correta: bool = avaliacao["correta"]
    feedback: str = avaliacao["feedback"]

    pontuacao_atual: int = rodada["pontuacao_atual"]
    penalidade = 0

    if correta:
        novo_status = "vitoria"
    else:
        penalidade = PENALIDADE_RESPOSTA_ERRADA
        pontuacao_atual = max(0, pontuacao_atual - penalidade)
        novo_status = "derrota" if pontuacao_atual <= 0 else "em_andamento"

    # Persistir tentativa
    db_tentativas.registrar_tentativa(
        rodada_id=rodada["id"],
        resposta_usuario=resposta_usuario,
        feedback_ia=feedback,
        correta=correta,
        penalidade_aplicada=penalidade,
    )

    # Atualizar pontuação e status da rodada
    db_rodadas.atualizar_pontuacao(rodada["id"], pontuacao_atual)

    if novo_status in ("vitoria", "derrota"):
        db_rodadas.finalizar_rodada(rodada["id"], novo_status)
        if novo_status == "vitoria":
            db_usuarios.atualizar_pontuacao(rodada["usuario_id"], pontuacao_atual)

    return ResultadoTentativa(
        correta=correta,
        feedback=feedback,
        pontuacao_atual=pontuacao_atual,
        penalidade=penalidade,
        status_rodada=novo_status,
    )


def usar_dica(rodada: dict, enigma: dict) -> dict:
    """
    Aplica penalidade da próxima dica e retorna o texto da dica.
    Retorna dict com 'texto_dica', 'penalidade', 'pontuacao_atual', 'dicas_usadas'.
    """
    dicas_usadas: int = rodada["dicas_usadas"]
    pontuacao_atual: int = rodada["pontuacao_atual"]

    if dicas_usadas >= 3:
        return {
            "texto_dica": "Todas as dicas já foram usadas.",
            "penalidade": 0,
            "pontuacao_atual": pontuacao_atual,
            "dicas_usadas": dicas_usadas,
        }

    proxima_dica = dicas_usadas + 1
    penalidade = PENALIDADE_DICA[proxima_dica]
    nova_pontuacao = max(0, pontuacao_atual - penalidade)

    dica_map = {1: enigma.get("dica_1"), 2: enigma.get("dica_2"), 3: enigma.get("dica_3")}
    texto_dica = dica_map[proxima_dica] or "Dica não disponível."

    # Persistir
    db_rodadas.atualizar_pontuacao(rodada["id"], nova_pontuacao)
    rodada_atualizada = db_rodadas.incrementar_dica(rodada["id"], dicas_usadas)
    novas_dicas = rodada_atualizada["dicas_usadas"] if rodada_atualizada else proxima_dica

    # Verificar derrota por pontuação
    if nova_pontuacao <= 0:
        db_rodadas.finalizar_rodada(rodada["id"], "derrota")

    return {
        "texto_dica": texto_dica,
        "penalidade": penalidade,
        "pontuacao_atual": nova_pontuacao,
        "dicas_usadas": novas_dicas,
    }


def iniciar_nova_rodada(usuario_id: str, enigma: dict) -> dict | None:
    """Cria uma nova rodada no banco e retorna o registro."""
    return db_rodadas.criar_rodada(
        usuario_id=usuario_id,
        enigma_id=enigma["id"],
        pontuacao_inicial=enigma["pontuacao_inicial"],
    )
