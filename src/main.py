# # Iniciando o banco de dados e populando os dados iniciais


def init_database_and_vector():
    from db.database import init_db
    from rag.vector import rebuild_vectorstore_from_sql
    from src.db.seed_init import init_seed

    init_db()
    init_seed()

    # Passando os dados para o vector store
    rebuild_vectorstore_from_sql()


# Iniciando a aplicação
# Chaves de configuração

# Iniciar a aplicação


def main():
    from engine.graph import EngineGraph

    engine = EngineGraph()
    graph = engine.build_graph()
    print("=== Finance AI Chat ===")
    print("Digite sua pergunta ou 'sair' para encerrar.\n")

    while True:
        question = input("Você: ")

        if question.lower() in ["s", "sair", "exit", "quit"]:
            print("Encerrado.")
            break

        resp = graph.invoke({"question": question}, config={"thread_id": "user-thread"})

        print("AI:", resp["answer"])
        print()


if __name__ == "__main__":
    # init_database_and_vector()
    main()
