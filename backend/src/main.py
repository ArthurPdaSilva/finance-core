from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.check_key import check_api_key

app = FastAPI()

origins = [
    "http://localhost:3000",
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


@app.post("/init-db")
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
    chat_history: list[str]
    chat_id: int | None = None


# cd src
# uvicorn main:app --reload
@app.post("/finance-ai")
def finance_ai_question(finance_question: FinanceQuestion):
    from langfuse import get_client
    from langfuse.langchain import CallbackHandler

    from engine.engine_graph import EngineGraph

    check_api_key(finance_question.key)

    engine = EngineGraph()
    graph = engine.build_graph()
    langfuse_handler = CallbackHandler()
    langfuse = get_client()

    with langfuse.start_as_current_span(name="user-question") as span:
        span.update_trace(name="user-question", input=finance_question.question)
        resp = graph.invoke(
            {
                "question": finance_question.question,
                "chat_history": finance_question.chat_history,
                "chat_id": finance_question.chat_id,
            },
            config={"thread_id": "user-thread", "callbacks": [langfuse_handler]},
        )

        span.update_trace(name="user-question", output=resp["answer"])
        return {"message": resp["answer"], "chat_id": resp["chat_id"]}


@app.get("/finance-ai/chats")
def chats(key: str):
    check_api_key(key)
    from db.database import SessionLocal
    from models.finance_models import Chat

    db = SessionLocal()
    db = SessionLocal()
    try:
        chats = db.query(Chat).order_by(Chat.criado_em.desc()).all()
        return {"status": "success", "count": len(chats), "data": chats}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@app.get("/finance-ai/messages")
def get_messages(chat_id: str, key: str):
    check_api_key(key)
    from fastapi import HTTPException

    from db.database import SessionLocal
    from models.finance_models import Message

    db = SessionLocal()
    try:
        messages = (
            db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.criado_em.desc())
            .all()
        )

        return {"status": "success", "count": len(messages), "data": messages}

    except HTTPException as he:
        raise he
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
