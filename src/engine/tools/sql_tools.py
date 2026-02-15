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
def atualizar_divida_tool(
    id: int,
    nome: str = None,
    valor_total: float = None,
    parcelas_restantes: int = None,
    usuario_id: int = None,
):
    """
    Atualiza uma dívida existente.

    Args:
        id: ID da dívida.
        nome: Novo nome da dívida (opcional).
        valor_total: Novo valor total (opcional).
        parcelas_restantes: Atualiza quantidade de parcelas restantes (opcional).
        usuario_id: Atualiza o dono da dívida (opcional).
    """
    db = SessionLocal()
    divida = db.query(Divida).filter(Divida.id == id).first()

    if not divida:
        db.close()
        return "Dívida não encontrada."

    if nome is not None:
        divida.nome = nome

    if valor_total is not None:
        divida.valor_total = valor_total

    if parcelas_restantes is not None:
        divida.parcelas_restantes = parcelas_restantes

    if usuario_id is not None:
        divida.usuario_id = usuario_id

    db.commit()
    db.refresh(divida)
    db.close()

    return json.dumps(
        {
            "id": divida.id,
            "nome": divida.nome,
            "valor_total": divida.valor_total,
            "parcelas_restantes": divida.parcelas_restantes,
            "usuario_id": divida.usuario_id,
            "status": "Dívida atualizada com sucesso.",
        }
    )


@tool
def remove_conta_tool(id: int):
    """
    Remove uma conta mensal pelo ID.
    """
    db = SessionLocal()
    conta_to_remove = db.query(ContaMensal).filter(ContaMensal.id == id).first()
    if conta_to_remove:
        db.delete(conta_to_remove)
        db.commit()
        status = "Conta removida."
    else:
        status = "Conta não encontrada."
    db.close()
    return status


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
def atualizar_conta_tool(
    id: int,
    nome: str = None,
    valor: float = None,
    usuario_id: int = None,
):
    """
    Atualiza uma conta mensal existente.

    Args:
        id: ID da conta.
        nome: Novo nome da conta (opcional).
        valor: Novo valor da conta (opcional).
        usuario_id: Novo usuário associado (opcional).
    """
    db = SessionLocal()
    conta = db.query(ContaMensal).filter(ContaMensal.id == id).first()

    if not conta:
        db.close()
        return "Conta não encontrada."

    if nome is not None:
        conta.nome = nome

    if valor is not None:
        conta.valor = valor

    if usuario_id is not None:
        conta.usuario_id = usuario_id

    db.commit()
    db.refresh(conta)
    db.close()

    return json.dumps(
        {
            "id": conta.id,
            "nome": conta.nome,
            "valor": conta.valor,
            "usuario_id": conta.usuario_id,
            "status": "Conta atualizada com sucesso.",
        }
    )


@tool
def remove_divida_tool(id: int):
    """
    Remove uma dívida pelo ID.
    """
    db = SessionLocal()
    divida_to_remove = db.query(Divida).filter(Divida.id == id).first()
    if divida_to_remove:
        db.delete(divida_to_remove)
        db.commit()
        status = "Dívida removida."
    else:
        status = "Dívida não encontrada."
    db.close()
    return status


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
def atualizar_usuario_tool(id: int, nome: str = None, salario: float = None):
    """
    Atualiza os dados de um usuário existente.

    Args:
        id: ID do usuário a ser atualizado.
        nome: Novo nome (opcional).
        salario: Novo salário (opcional).
    """

    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        db.close()
        return "Usuário não encontrado."

    # Atualiza apenas os campos enviados
    if nome is not None:
        usuario.nome = nome

    if salario is not None:
        usuario.salario = salario

    db.commit()
    db.refresh(usuario)
    db.close()

    return json.dumps(
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "salario": usuario.salario,
            "status": "Usuário atualizado com sucesso.",
        }
    )


@tool
def remove_usuario_tool(id: int):
    """
    Remove um usuário pelo ID.
    """
    db = SessionLocal()
    usuario_to_remove = db.query(Usuario).filter(Usuario.id == id).first()
    if usuario_to_remove:
        db.delete(usuario_to_remove)
        db.commit()
        status = "Usuário removido."
    else:
        status = "Usuário não encontrado."
    db.close()
    return status
