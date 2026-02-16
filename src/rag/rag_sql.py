from langchain_core.documents import Document

from db.database import SessionLocal
from models.finance_models import ContaMensal, Divida, Usuario


def sql_to_documents():
    db = SessionLocal()
    docs = []
    usuarios_map = {u.id: u for u in db.query(Usuario).all()}

    # Usuario
    for u in db.query(Usuario).all():
        text = f"UsuárioID: {u.id}. Nome: {u.nome}. Salário: {u.salario} reais."
        docs.append(Document(page_content=text))

    # CONTAS MENSAIS
    for c in db.query(ContaMensal).all():
        usuario = usuarios_map[c.usuario_id]
        text = (
            f"Conta mensal: {c.nome}. "
            f"Valor: {c.valor} reais. "
            f"UsuárioID: {c.usuario_id}."
            f"UsuarioNome: {usuario.nome}"
        )
        docs.append(Document(page_content=text))

    # DIVIDAS
    for d in db.query(Divida).all():
        usuario = usuarios_map[d.usuario_id]
        text = (
            f"Dívida: {d.nome}. "
            f"Valor total: {d.valor_total} reais. "
            f"Parcelas restantes: {d.parcelas_restantes}. "
            f"UsuárioID: {d.usuario_id}."
            f"UsuarioNome: {usuario.nome}"
        )
        docs.append(Document(page_content=text))

    db.close()
    return docs
