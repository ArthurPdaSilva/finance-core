from langchain_core.documents import Document

from db.database import SessionLocal
from models.finance_models import (
    RegistroFinanceiro,
    TipoTransacao,
    Usuario,
)


def sql_to_documents():
    db = SessionLocal()
    docs = []
    usuarios_map = {u.id: u for u in db.query(Usuario).all()}

    # Usuario
    for u in db.query(Usuario).all():
        text = f"UsuárioID: {u.id}. Nome: {u.nome}. Salário: {u.salario} reais."
        docs.append(Document(page_content=text))

    # REGISTROS FINANCEIROS
    registros = db.query(RegistroFinanceiro).all()

    for r in registros:
        usuario = usuarios_map[r.usuario_id]

        # Tipo legível
        tipo_str = "Conta mensal" if r.tipo == TipoTransacao.CONTA else "Dívida"

        # Montagem do texto base
        text = (
            f"{tipo_str}: {r.nome}. "
            f"Valor por parcela: {r.valor_por_parcela:.2f} reais. "
            f"UsuárioID: {r.usuario_id}. "
            f"UsuarioNome: {usuario.nome}. "
        )

        # Se tiver valor total, adiciona
        if r.valor_total is not None:
            text += f"Valor total: {r.valor_total:.2f} reais. "

        # Se tiver parcelas restantes, adiciona
        if r.parcelas_restantes is not None:
            text += f"Parcelas restantes: {r.parcelas_restantes}. "

        docs.append(Document(page_content=text))

    db.close()
    return docs
