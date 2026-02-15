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
