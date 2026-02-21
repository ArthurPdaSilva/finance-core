from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.check_key import check_api_key

app = FastAPI()

origins = [
    "http://localhost:3000",  # seu front local
    "https://finance-app-kappa-two.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class InitDb(BaseModel):
    key: str


@app.get("/init-db")
def init_database_and_vector_store(init_db: InitDb):
    # Iniciando o banco de dados e populando os dados iniciais
    check_api_key(init_db.key)

    def init_database_and_vector():
        from db.database import init_db
        from db.seed_init import init_seed
        from rag.vector import rebuild_vectorstore_from_sql

        init_db()
        init_seed()

        # Passando os dados para o vector store
        rebuild_vectorstore_from_sql()

    init_database_and_vector()
    return {"message": "Banco de dados e vector store inicializados com sucesso!"}


class FinanceQuestion(BaseModel):
    question: str
    key: str


# cd src
# uvicorn main:app --reload
@app.post("/finance-ai")
def finance_ai_question(question: FinanceQuestion):
    from langfuse import get_client
    from langfuse.langchain import CallbackHandler

    from engine.engine_graph import EngineGraph

    check_api_key(question.key)

    engine = EngineGraph()
    graph = engine.build_graph()
    langfuse_handler = CallbackHandler()
    langfuse = get_client()

    with langfuse.start_as_current_span(name="user-question") as span:
        span.update_trace(name="user-question", input=question)
        resp = graph.invoke(
            {"question": question.question},
            config={"thread_id": "user-thread", "callbacks": [langfuse_handler]},
        )

        span.update_trace(name="user-question", output=resp["answer"])
        return {"message": resp["answer"]}
