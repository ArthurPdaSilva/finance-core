import json

from langchain.tools import tool

from db.database import SessionLocal
from models.finance_models import ContaMensal, Divida, Usuario

# --------------------------
#         CONTAS
# --------------------------


@tool
def add_conta_tool(nome: str, valor: float, usuario_id: int = 1):
    """
    Adiciona uma conta mensal no banco de dados.

    Args:
        nome: Nome da conta.
        valor: Valor da conta.
        usuario_id: Usuário dono da conta (default=1).
    """
    db = SessionLocal()
    conta = ContaMensal(
        nome=nome,
        valor=valor,
        usuario_id=usuario_id,
    )
    db.add(conta)
    db.commit()
    db.refresh(conta)
    db.close()
    return json.dumps({"id": conta.id, "nome": conta.nome, "valor": conta.valor})


@tool
def atualizar_conta_por_nome_tool(
    nome_atual: str,
    novo_nome: str = None,
    novo_valor: float = None,
    usuario_id: int = None,
):
    """
    Atualiza uma conta buscando pelo nome, sem expor IDs ao LLM.
    """

    db = SessionLocal()
    conta = db.query(ContaMensal).filter(ContaMensal.nome == nome_atual).first()

    if not conta:
        db.close()
        return "Conta não encontrada pelo nome informado."

    if novo_nome is not None:
        conta.nome = novo_nome

    if novo_valor is not None:
        conta.valor = novo_valor

    if usuario_id is not None:
        conta.usuario_id = usuario_id

    db.commit()
    db.refresh(conta)
    db.close()

    return json.dumps(
        {
            "nome": conta.nome,
            "valor": conta.valor,
            "status": "Conta atualizada com sucesso.",
        }
    )


@tool
def remover_conta_por_nome_tool(nome: str):
    """
    Remove uma conta pelo nome sem expor ID ao agente.
    """

    db = SessionLocal()
    conta = db.query(ContaMensal).filter(ContaMensal.nome == nome).first()

    if not conta:
        db.close()
        return "Conta não encontrada."

    db.delete(conta)
    db.commit()
    db.close()

    return "Conta removida com sucesso."


# --------------------------
#         DÍVIDAS
# --------------------------


@tool
def add_divida_tool(
    nome: str,
    valor_total: float,
    parcelas_restantes: int,
    usuario_id: int = 1,
):
    """
    Adiciona uma dívida no banco.

    Args:
        nome: Nome da dívida.
        valor_total: Valor total devido.
        parcelas_restantes: Número de parcelas finais.
        usuario_id: Dono da dívida.
    """
    db = SessionLocal()
    d = Divida(
        nome=nome,
        valor_total=valor_total,
        parcelas_restantes=parcelas_restantes,
        usuario_id=usuario_id,
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    db.close()

    return json.dumps(
        {
            "id": d.id,
            "nome": d.nome,
            "valor_total": d.valor_total,
            "parcelas_restantes": d.parcelas_restantes,
        }
    )


@tool
def atualizar_divida_por_nome_tool(
    nome_atual: str,
    novo_nome: str = None,
    novo_valor_total: float = None,
    novas_parcelas: int = None,
    usuario_id: int = None,
):
    """
    Atualiza uma dívida pelo nome, sem expor IDs ao modelo.
    """

    db = SessionLocal()
    divida = db.query(Divida).filter(Divida.nome == nome_atual).first()

    if not divida:
        db.close()
        return "Dívida não encontrada pelo nome informado."

    if novo_nome is not None:
        divida.nome = novo_nome

    if novo_valor_total is not None:
        divida.valor_total = novo_valor_total

    if novas_parcelas is not None:
        divida.parcelas_restantes = novas_parcelas

    if usuario_id is not None:
        divida.usuario_id = usuario_id

    db.commit()
    db.refresh(divida)
    db.close()

    return json.dumps(
        {
            "nome": divida.nome,
            "valor_total": divida.valor_total,
            "parcelas_restantes": divida.parcelas_restantes,
            "status": "Dívida atualizada.",
        }
    )


@tool
def remover_divida_por_nome_tool(nome: str):
    """
    Remove uma dívida pelo nome sem expor ID ao agente.
    """

    db = SessionLocal()
    divida = db.query(Divida).filter(Divida.nome == nome).first()

    if not divida:
        db.close()
        return "Dívida não encontrada."

    db.delete(divida)
    db.commit()
    db.close()

    return "Dívida removida com sucesso."


# --------------------------
#        USUÁRIOS
# --------------------------


@tool
def add_usuario_tool(nome: str, salario: float):
    """
    Adiciona um usuário ao banco.

    Args:
        nome: Nome do usuário.
        salario: Salário associado.
    """
    db = SessionLocal()
    usuario = Usuario(nome=nome, salario=salario)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    db.close()

    return json.dumps(
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "salario": usuario.salario,
        }
    )


@tool
def atualizar_usuario_por_nome_tool(
    nome_atual: str,
    novo_nome: str = None,
    novo_salario: float = None,
):
    """
    Atualiza um usuário buscando pelo nome, sem expor IDs.
    """

    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.nome == nome_atual).first()

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
    Remove um usuário sem expor ID.
    """

    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.nome == nome).first()

    if not usuario:
        db.close()
        return "Usuário não encontrado."

    db.delete(usuario)
    db.commit()
    db.close()

    return "Usuário removido com sucesso."
