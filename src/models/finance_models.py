import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    salario = Column(Float, nullable=False)


class TipoTransacao(str, enum.Enum):
    CONTA = "conta"
    DIVIDA = "divida"


class RegistroFinanceiro(Base):
    __tablename__ = "registros_financeiros"

    id = Column(Integer, primary_key=True)
    tipo = Column(
        Enum(TipoTransacao, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
    )

    nome = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    valor_por_parcela = Column(Float, nullable=False)

    valor_total = Column(Float, nullable=True)
    parcelas_restantes = Column(Integer, nullable=True)
