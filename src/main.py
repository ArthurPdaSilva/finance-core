# Iniciando o banco de dados e populando os dados iniciais
# from src.db.database import init_db
# from src.db.seed import init_seed


# init_db()
# init_seed()

# Passando os dados para o vector store
# from src.rag.vector import rebuild_vectorstore_from_sql

# rebuild_vectorstore_from_sql()

# Iniciando a aplicação
# Chaves de configuração

# Iniciar a aplicação

from engine.graph import EngineGraph

engine = EngineGraph()
graph = engine.build_graph()

# Passar o dicionário configurável corretamente dentro de `kwargs`
resp = graph.invoke(
    {
        "question": "Qual o total que pago em aluguel, meu lindo",
    },
    config={
        "thread_id": "arthur-thread"  # pode ser qualquer string
    },
)


print(resp["answer"])
