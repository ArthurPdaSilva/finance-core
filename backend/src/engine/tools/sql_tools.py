import json

from langchain.tools import tool
from sqlalchemy import func

from db.database import SessionLocal
from models.finance_models import (
    Chat,
    Message,
    RegistroFinanceiro,
    TipoTransacao,
    Usuario,
)

# ==========================================================
#                 REGISTROS FINANCEIROS
# ==========================================================


def get_usuario_id_by_nome(db, nome: str | None):
    """Busca o ID do usuário pelo nome, retornando 1 como padrão."""
    if not nome:
        return 1  # fallback seguro

    usuario = db.query(Usuario).filter(func.lower(Usuario.nome) == nome.lower()).first()

    if not usuario:
        return 1  # fallback silencioso (não quebra a tool)

    return usuario.id


@tool
def add_registro_tool(
    nome: str,
    tipo: str,
    usuario_nome: str = None,
    valor: float = None,
    valor_total: float = None,
    parcelas_restantes: int = None,
):
    """
    Cria um registro financeiro unificado (conta ou dívida).

    Para CONTAS:
        - tipo="conta"
        - valor (obrigatório)

    Para DÍVIDAS:
        - tipo="divida"
        - valor_total e parcelas_restantes obrigatórios
    """

    db = SessionLocal()

    tipo_enum = TipoTransacao(tipo)

    if tipo_enum == TipoTransacao.CONTA:
        if valor is None:
            return "Conta precisa de 'valor'."
        valor_por_parcela = valor
        valor_total = None
        parcelas_restantes = None

    elif tipo_enum == TipoTransacao.DIVIDA:
        if valor_total is None or parcelas_restantes is None:
            return "Dívida precisa de 'valor_total' e 'parcelas_restantes'."
        valor_por_parcela = valor_total / parcelas_restantes

    usuario_id = get_usuario_id_by_nome(db, usuario_nome)

    registro = RegistroFinanceiro(
        nome=nome,
        tipo=tipo_enum,
        usuario_id=usuario_id,
        valor_por_parcela=valor_por_parcela,
        valor_total=valor_total,
        parcelas_restantes=parcelas_restantes,
    )

    db.add(registro)
    db.commit()
    db.refresh(registro)
    db.close()

    return json.dumps(
        {
            "id": registro.id,
            "nome": registro.nome,
            "tipo": registro.tipo.value,
            "valor_por_parcela": registro.valor_por_parcela,
        }
    )


@tool
def atualizar_registro_por_nome_tool(
    nome_atual: str,
    novo_nome: str = None,
    novo_valor: float = None,
    novo_valor_total: float = None,
    novas_parcelas: int = None,
    novo_tipo: str = None,
):
    """
    Atualiza qualquer registro financeiro (conta ou dívida) pelo NOME.
    """

    db = SessionLocal()
    registro = (
        db.query(RegistroFinanceiro)
        .filter(func.lower(RegistroFinanceiro.nome) == nome_atual.lower())
        .first()
    )

    if not registro:
        db.close()
        return "Registro financeiro não encontrado."

    # Atualiza nome
    if novo_nome is not None:
        registro.nome = novo_nome

    # Atualiza tipo
    if novo_tipo is not None:
        registro.tipo = TipoTransacao(novo_tipo)

    # Atualiza conta (valor único)
    if registro.tipo == TipoTransacao.CONTA:
        if novo_valor is not None:
            registro.valor_por_parcela = novo_valor
        registro.valor_total = None
        registro.parcelas_restantes = None

    # Atualiza dívida
    if registro.tipo == TipoTransacao.DIVIDA:
        if novo_valor_total is not None:
            registro.valor_total = novo_valor_total

        if novas_parcelas is not None:
            registro.parcelas_restantes = novas_parcelas

        if registro.valor_total and registro.parcelas_restantes:
            registro.valor_por_parcela = (
                registro.valor_total / registro.parcelas_restantes
            )

    db.commit()
    db.refresh(registro)
    db.close()

    return json.dumps(
        {
            "nome": registro.nome,
            "tipo": registro.tipo.value,
            "valor_por_parcela": registro.valor_por_parcela,
            "status": "Registro atualizado com sucesso.",
        }
    )


@tool
def remover_registro_por_nome_tool(nome: str):
    """
    Remove qualquer registro financeiro pelo nome.
    """

    db = SessionLocal()
    registro = (
        db.query(RegistroFinanceiro)
        .filter(func.lower(RegistroFinanceiro.nome) == nome.lower())
        .first()
    )

    if not registro:
        db.close()
        return "Registro financeiro não encontrado."

    db.delete(registro)
    db.commit()
    db.close()

    return "Registro removido com sucesso."


@tool
def alterar_usuario_do_registro_por_nome_tool(nome: str, novo_usuario_nome: str):
    """
    Altera o usuário associado a um registro financeiro pelo nome do registro.
    """

    db = SessionLocal()
    registro = (
        db.query(RegistroFinanceiro)
        .filter(func.lower(RegistroFinanceiro.nome) == nome.lower())
        .first()
    )

    if not registro:
        db.close()
        return "Registro financeiro não encontrado."

    novo_usuario_id = get_usuario_id_by_nome(db, novo_usuario_nome)

    registro.usuario_id = novo_usuario_id
    db.commit()
    db.refresh(registro)
    db.close()

    return json.dumps(
        {
            "nome": registro.nome,
            "novo_usuario_id": registro.usuario_id,
            "status": "Usuário do registro atualizado com sucesso.",
        }
    )


# ==========================================================
#                        USUÁRIOS
# ==========================================================


@tool
def add_usuario_tool(nome: str, salario: float):
    """
    Cadastra um novo usuário no sistema.
    Recebe o nome do usuário e o valor do salário mensal.
    """
    db = SessionLocal()
    usuario = Usuario(nome=nome, salario=salario)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    db.close()

    return json.dumps(
        {"id": usuario.id, "nome": usuario.nome, "salario": usuario.salario}
    )


@tool
def atualizar_usuario_por_nome_tool(
    nome_atual: str,
    novo_nome: str = None,
    novo_salario: float = None,
):
    """
    Atualiza as informações de um usuário existente pesquisando pelo nome atual.
    Permite alterar o nome ou o salário.
    """
    db = SessionLocal()
    usuario = (
        db.query(Usuario).filter(func.lower(Usuario.nome) == nome_atual.lower()).first()
    )

    if not usuario:
        db.close()
        return "Usuário não encontrado."

    if novo_nome is not None:
        usuario.nome = novo_nome

    if novo_salario is not None:
        usuario.salario = novo_salario

    db.commit()
    db.refresh(usuario)
    db.close()

    return json.dumps(
        {
            "nome": usuario.nome,
            "salario": usuario.salario,
            "status": "Usuário atualizado.",
        }
    )


@tool
def remover_usuario_por_nome_tool(nome: str):
    """
    Remove permanentemente um usuário do banco de dados pelo seu nome.
    """
    db = SessionLocal()
    usuario = db.query(Usuario).filter(func.lower(Usuario.nome) == nome.lower()).first()

    if not usuario:
        db.close()
        return "Usuário não encontrado."

    db.delete(usuario)
    db.commit()
    db.close()

    return "Usuário removido com sucesso."


# ==========================================================
#                        CHAT
# ==========================================================


@tool
def criar_ou_buscar_chat_tool(titulo: str, chat_id: int | None = None):
    """
    Cria um novo chat ou retorna um existente.
    Se chat_id for fornecido, tenta buscar; se nulo, cria um novo com o título.
    """
    db = SessionLocal()
    try:
        if chat_id:
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if chat:
                return json.dumps(
                    {"chat_id": chat.id, "titulo": chat.titulo, "status": "existente"}
                )

        if db.query(Chat).filter(Chat.titulo == titulo).first():
            return json.dumps(
                {
                    "chat_id": None,
                    "titulo": titulo,
                    "status": "Chat com esse nome já existe",
                }
            )

        novo_chat = Chat(titulo=titulo)

        db.add(novo_chat)
        db.commit()
        db.refresh(novo_chat)
        return json.dumps(
            {"chat_id": novo_chat.id, "titulo": novo_chat.titulo, "status": "criado"}
        )
    finally:
        db.close()


@tool
def salvar_turno_conversa_tool(chat_id: int, question: str, answer: str):
    """
    Salva o par pergunta (user) e resposta (assistant) de uma vez no chat.
    """
    db = SessionLocal()
    try:
        msg_user = Message(chat_id=chat_id, role="user", content=question)
        msg_ai = Message(chat_id=chat_id, role="assistant", content=answer)

        db.add_all([msg_user, msg_ai])  # Salva ambos na mesma transação
        db.commit()

        return json.dumps({"status": "turno salvo", "chat_id": chat_id})
    except Exception as e:
        db.rollback()
        return json.dumps({"status": "erro", "message": str(e)})
    finally:
        db.close()
