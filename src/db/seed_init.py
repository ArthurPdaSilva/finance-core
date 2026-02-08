import os
import sqlite3

from dotenv import load_dotenv

from src.db.seeds import CONTAS, DIVIDAS, USUARIOS

load_dotenv()

DB_NAME = os.getenv("DATABASE_NAME") or "database.sqlite3"

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
    CREATE TABLE IF NOT EXISTS contas_mensais (
        id INTEGER PRIMARY KEY,
        usuario_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        valor REAL NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS dividas (
        id INTEGER PRIMARY KEY,
        usuario_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        valor_total REAL NOT NULL,
        parcelas_restantes INTEGER NOT NULL,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """,
]


# ---------------------------------------------------------
# Funções utilitárias
# ---------------------------------------------------------


def create_tables(cursor):
    for query in CREATE_TABLES:
        cursor.execute(query)


def clear_tables(cursor):
    # Deleta tudo para permitir rodar várias vezes
    cursor.execute("DELETE FROM dividas")
    cursor.execute("DELETE FROM contas_mensais")
    cursor.execute("DELETE FROM usuarios")


def seed_data(cursor):
    cursor.executemany(
        "INSERT INTO usuarios (id, nome, salario) VALUES (?, ?, ?)", USUARIOS
    )
    cursor.executemany(
        "INSERT INTO contas_mensais (id, usuario_id, nome, valor) VALUES (?, ?, ?, ?)",
        CONTAS,
    )
    cursor.executemany(
        "INSERT INTO dividas (id, usuario_id, nome, valor_total, parcelas_restantes) VALUES (?, ?, ?, ?, ?)",
        DIVIDAS,
    )


# ---------------------------------------------------------
# Execução principal
# ---------------------------------------------------------


def init_seed():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    create_tables(cursor)
    clear_tables(cursor)
    seed_data(cursor)

    conn.commit()
    conn.close()

    print("Seed executado com sucesso!")
