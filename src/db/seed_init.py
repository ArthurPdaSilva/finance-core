import sqlite3

from config.secrets import Secrets
from db.seeds import REGISTROS_FINANCEIROS, USUARIOS
from models.finance_models import TipoTransacao

DB_NAME = Secrets.DATABASE_NAME or "database.sqlite3"

# ---------------------------------------------------------
# Criação / Remoção de Tabelas
# ---------------------------------------------------------

DROP_OLD_TABLES = [
    "DROP TABLE IF EXISTS contas_mensais",
    "DROP TABLE IF EXISTS dividas",
]

# ---------------------------------------------------------
# Criação das tabelas (somente exemplo – edite se já existem)
# ---------------------------------------------------------
CREATE_TABLES = [
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
        tipo TEXT NOT NULL CHECK(tipo IN ('conta', 'divida')),                -- conta | divida
        nome TEXT NOT NULL,
        valor_por_parcela REAL NOT NULL,               -- valor da conta ou parcela
        valor_total REAL,                  -- apenas dívidas
        parcelas_restantes INTEGER,        -- apenas dívidas
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """,
]


# ---------------------------------------------------------
# Funções utilitárias
# ---------------------------------------------------------


def drop_old_tables(cursor):
    for query in DROP_OLD_TABLES:
        cursor.execute(query)


def create_tables(cursor):
    for query in CREATE_TABLES:
        cursor.execute(query)


def clear_tables(cursor):
    cursor.execute("DELETE FROM registros_financeiros")
    cursor.execute("DELETE FROM usuarios")


def seed_data(cursor):
    # Usuários
    cursor.executemany(
        "INSERT INTO usuarios (id, nome, salario) VALUES (?, ?, ?)",
        USUARIOS,
    )

    # Registros Financeiros
    for registro in REGISTROS_FINANCEIROS:
        if isinstance(registro["tipo"], TipoTransacao):
            registro["tipo"] = registro["tipo"].value

    cursor.executemany(
        """
        INSERT INTO registros_financeiros 
        (id, usuario_id, tipo, nome, valor_por_parcela, valor_total, parcelas_restantes)
        VALUES (:id, :usuario_id, :tipo, :nome, :valor_por_parcela, :valor_total, :parcelas_restantes)
        """,
        REGISTROS_FINANCEIROS,
    )


# ---------------------------------------------------------
# Execução principal
# ---------------------------------------------------------


def init_seed():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    drop_old_tables(cursor)
    create_tables(cursor)
    clear_tables(cursor)
    seed_data(cursor)

    conn.commit()
    conn.close()

    print("Seed executado com sucesso!")
