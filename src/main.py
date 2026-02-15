# # Iniciando o banco de dados e populando os dados iniciais


def init_database_and_vector():
    from db.database import init_db
    from db.seed_init import init_seed
    from rag.vector import rebuild_vectorstore_from_sql

    init_db()
    init_seed()

    # Passando os dados para o vector store
    rebuild_vectorstore_from_sql()


# Iniciando a aplicação
# Chaves de configuração

# Iniciar a aplicação


def main():
    from langfuse import get_client
    from langfuse.langchain import CallbackHandler

    from engine.engine_graph import EngineGraph

    engine = EngineGraph()
    graph = engine.build_graph()
    print("=== Finance AI Chat ===")
    print("Digite sua pergunta ou 'sair' para encerrar.\n")
    langfuse_handler = CallbackHandler()
    langfuse = get_client()

    while True:
        question = input("Você: ")

        if question.lower() in ["s", "sair", "exit", "quit"]:
            print("Encerrado.")
            break

        with langfuse.start_as_current_span(name="user-question") as span:
            span.update_trace(name="user-question", input=question)
            resp = graph.invoke(
                {"question": question},
                config={"thread_id": "user-thread", "callbacks": [langfuse_handler]},
            )

            span.update_trace(name="user-question", output=resp["answer"])
        print("AI:", resp["answer"])


if __name__ == "__main__":
    # init_database_and_vector()
    main()


# TODOS
# Adicionar tool de update
# Adicionar Langfuse
# Adicionar fastapi
