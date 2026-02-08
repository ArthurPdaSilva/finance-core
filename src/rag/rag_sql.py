from langchain_core.documents import Document

from db.database import SessionLocal
from models.finance_models import ContaMensal, Divida, Usuario


def sql_to_documents():
    db = SessionLocal()
    docs = []

    # Usuario
    for u in db.query(Usuario).all():
        text = f"Usuário: {u.nome}. Salário: {u.salario} reais."
        docs.append(
            Document(page_content=text, metadata={"table": "usuarios", "id": u.id})
        )

    # CONTAS MENSAIS
    for c in db.query(ContaMensal).all():
        text = f"Conta mensal: {c.nome}. Valor: {c.valor} reais."
        docs.append(
            Document(
                page_content=text, metadata={"table": "contas_mensais", "id": c.id}
            )
        )

    # DIVIDAS
    for d in db.query(Divida).all():
        text = (
            f"Dívida: {d.nome}. Valor total: {d.valor_total}. "
            f"Parcelas restantes: {d.parcelas_restantes}. "
            f"Valor por parcela: {d.valor_por_parcela}."
        )
        docs.append(
            Document(page_content=text, metadata={"table": "dividas", "id": d.id})
        )

    db.close()
    return docs
