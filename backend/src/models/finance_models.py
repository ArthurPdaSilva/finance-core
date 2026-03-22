from datetime import datetime, timezone
import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, unique=True)
    titulo = Column(String, nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_token = Column(String, ForeignKey("chats.token"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    chat = relationship("Chat", backref="messages")


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
