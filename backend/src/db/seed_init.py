from sqlalchemy import text

from db.database import engine
from db.seeds import REGISTROS_FINANCEIROS, USUARIOS
from models.finance_models import TipoTransacao

AUTO_ID = "SERIAL PRIMARY KEY" if engine.dialect.name == "postgresql" else "INTEGER PRIMARY KEY"

# ---------------------------------------------------------
# Criação / Remoção de Tabelas
# ---------------------------------------------------------

DROP_OLD_TABLES = [
    "DROP TABLE IF EXISTS contas_mensais",
    "DROP TABLE IF EXISTS dividas",
    # Novas para histórico de chat:
    "DROP TABLE IF EXISTS messages",
    "DROP TABLE IF EXISTS chats",
]

# ---------------------------------------------------------
# Criação das tabelas
# ---------------------------------------------------------

CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        token_hash TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
        revoked_at TIMESTAMP WITH TIME ZONE,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        salario REAL NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS registros_financeiros (
        id INTEGER PRIMARY KEY,
        usuario_id INTEGER NOT NULL,
        tipo TEXT NOT NULL CHECK(tipo IN ('conta', 'divida')),
        nome TEXT NOT NULL,
        valor_por_parcela REAL NOT NULL,
        valor_total REAL,
        parcelas_restantes INTEGER,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """,
    # -----------------------------------------------------
    #  NOVAS TABELAS: CHAT + MESSAGES
    # -----------------------------------------------------
    f"""
    CREATE TABLE IF NOT EXISTS chats (
        id {AUTO_ID},
        token TEXT UNIQUE NOT NULL,
        titulo TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """,
    f"""
    CREATE TABLE IF NOT EXISTS messages (
        id {AUTO_ID},
        chat_token TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
        content TEXT NOT NULL,
        criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(chat_token) REFERENCES chats(token)
    )
    """,
]

# ---------------------------------------------------------
# Funções utilitárias
# ---------------------------------------------------------


def drop_old_tables(cursor):
    for query in DROP_OLD_TABLES:
        cursor.execute(text(query))


def create_tables(cursor):
    for query in CREATE_TABLES:
        cursor.execute(text(query))


def clear_tables(cursor):
    cursor.execute(text("DELETE FROM registros_financeiros"))
    cursor.execute(text("DELETE FROM usuarios"))


def seed_data(cursor):
    # Usuários
    cursor.execute(
        text("INSERT INTO usuarios (id, nome, salario) VALUES (:id, :nome, :salario)"),
        [{"id": user[0], "nome": user[1], "salario": user[2]} for user in USUARIOS],
    )

    # Registros Financeiros
    for registro in REGISTROS_FINANCEIROS:
        if isinstance(registro["tipo"], TipoTransacao):
            registro["tipo"] = registro["tipo"].value

    cursor.execute(
        text("""
        INSERT INTO registros_financeiros 
        (id, usuario_id, tipo, nome, valor_por_parcela, valor_total, parcelas_restantes)
        VALUES (:id, :usuario_id, :tipo, :nome, :valor_por_parcela, :valor_total, :parcelas_restantes)
        """),
        REGISTROS_FINANCEIROS,
    )


# ---------------------------------------------------------
# Execução principal
# ---------------------------------------------------------


def init_seed():
    with engine.begin() as conn:
        drop_old_tables(conn)
        create_tables(conn)
        clear_tables(conn)
        seed_data(conn)

    print("Seed executado com sucesso!")
