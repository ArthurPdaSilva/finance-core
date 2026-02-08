import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

def init_seed():
  conn = sqlite3.connect(os.getenv("DATABASE_NAME"))
  cursor = conn.cursor()

  cursor.execute("""
  INSERT INTO usuarios (id, nome, salario) VALUES
  (1, 'Arthur', 7500.00),
  (2, 'Mariana', 6800.00),
  (3, 'João Pedro', 5200.00)
  """)

  cursor.execute("""
  INSERT INTO contas_mensais (id, usuario_id, nome, valor) VALUES
  (1, 1, 'Aluguel', 1500.00),
  (2, 1, 'Internet', 120.00),
  (3, 1, 'Energia', 230.00),
  (4, 1, 'Academia', 45.00),
  (5, 2, 'Aluguel', 1350.00),
  (6, 2, 'Energia', 210.00),
  (7, 3, 'Condomínio', 320.00),
  (8, 3, 'Internet', 100.00)
  """)

  cursor.execute("""
  INSERT INTO dividas (id, usuario_id, nome, valor_total, parcelas_restantes) VALUES
  (1, 1, 'Cartão Nubank', 3200.00, 6),
  (2, 1, 'Moto Honda', 14500.00, 22),
  (3, 2, 'Notebook Dell', 5800.00, 4),
  (4, 3, 'Curso de Programação', 2400.00, 3)
  """)

  conn.commit()
  conn.close()

  print("Dados inseridos!")
