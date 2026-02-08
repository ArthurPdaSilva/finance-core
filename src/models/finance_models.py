from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    salario = Column(Float, nullable=False)


class ContaMensal(Base):
    __tablename__ = "contas_mensais"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)


class Divida(Base):
    __tablename__ = "dividas"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    valor_total = Column(Float, nullable=False)
    parcelas_restantes = Column(Integer, nullable=False)
    valor_por_parcela = Column(Float, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
