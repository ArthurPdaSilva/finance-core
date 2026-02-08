# # Iniciando o banco de dados e populando os dados iniciais
# from db.database import init_db
# from db.seed import init_seed
# from rag.vector import rebuild_vectorstore_from_sql

# init_db()
# init_seed()

# # Passando os dados para o vector store
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
        "question": "Quantas parcelas o Arthur tem q pagar da Carajas?",
    },
    config={
        "thread_id": "user-thread"  # pode ser qualquer string
    },
)


print(resp["answer"])
