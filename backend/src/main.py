from contextlib import asynccontextmanager
from datetime import datetime, timezone
import os

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from auth import (
    create_session,
    get_current_session,
    get_current_user,
    get_session_token,
    hash_session_token,
    normalize_email,
    password_hash,
    user_context,
)
from db.database import SessionLocal, engine
from models.finance_models import AuthUser, Base, Chat, Message, UserSession
from utils.check_key import check_api_key


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://frontend:3000",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


class InitDb(BaseModel):
    key: str


class SignupRequest(BaseModel):
    email: str
    password: str
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str


def user_response(user: AuthUser):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at,
    }


def auth_response(user: AuthUser, token: str):
    return {"token": token, "user": user_response(user)}


@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: SignupRequest):
    email = normalize_email(credentials.email)
    name = credentials.name.strip()
    if "@" not in email or len(email) > 255:
        raise HTTPException(status_code=422, detail="Informe um email válido.")
    if len(credentials.password) < 8:
        raise HTTPException(
            status_code=422, detail="A senha deve ter pelo menos 8 caracteres."
        )
    if not name or len(name) > 120:
        raise HTTPException(status_code=422, detail="Informe um nome válido.")

    db = SessionLocal()
    try:
        if db.query(AuthUser).filter(AuthUser.email == email).first():
            raise HTTPException(
                status_code=409, detail="Não foi possível criar a conta."
            )
        user = AuthUser(
            email=email,
            password_hash=password_hash.hash(credentials.password),
            name=name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_session(db, user)
        return auth_response(user, token)
    finally:
        db.close()


@app.post("/auth/login")
def login(credentials: LoginRequest):
    db = SessionLocal()
    try:
        user = (
            db.query(AuthUser)
            .filter(AuthUser.email == normalize_email(credentials.email))
            .first()
        )
        if not user or not password_hash.verify(
            credentials.password, user.password_hash
        ):
            raise HTTPException(status_code=401, detail="Email ou senha inválidos.")
        token = create_session(db, user)
        return auth_response(user, token)
    finally:
        db.close()


@app.get("/auth/me")
def me(current_user: AuthUser = Depends(get_current_user)):  # noqa: B008
    return user_response(current_user)


@app.post("/auth/logout")
def logout(
    authorization: str | None = Header(default=None),
    session=Depends(get_current_session),  # noqa: B008
):
    token = get_session_token(authorization)
    db = SessionLocal()
    try:
        stored_session = (
            db.query(UserSession)
            .filter(UserSession.token_hash == hash_session_token(token))
            .first()
        )
        if stored_session:
            stored_session.revoked_at = datetime.now(timezone.utc)
            db.commit()
        return {"message": "Sessão encerrada."}
    finally:
        db.close()


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
    chat_history: list[str]
    chat_token: str | None = None


# cd src
# uvicorn main:app --reload
@app.post("/finance-ai")
def finance_ai_question(
    finance_question: FinanceQuestion,
    current_user: AuthUser = Depends(get_current_user),  # noqa: B008
):
    from langfuse import get_client
    from langfuse.langchain import CallbackHandler

    from engine.engine_graph import EngineGraph

    engine = EngineGraph()
    graph = engine.build_graph()
    langfuse_handler = CallbackHandler()
    langfuse = get_client()

    with user_context(current_user.id):
        with langfuse.start_as_current_span(name="user-question") as span:
            span.update_trace(name="user-question", input=finance_question.question)
            resp = graph.invoke(
                {
                    "question": finance_question.question,
                    "chat_history": finance_question.chat_history,
                    "chat_token": finance_question.chat_token,
                    "user_id": current_user.id,
                },
                config={"thread_id": "user-thread", "callbacks": [langfuse_handler]},
            )

            span.update_trace(name="user-question", output=resp["answer"])
            return {"message": resp["answer"], "chat_token": resp["chat_token"]}


@app.get("/finance-ai/chats")
def chats(current_user: AuthUser = Depends(get_current_user)):  # noqa: B008
    db = SessionLocal()
    try:
        chats = (
            db.query(Chat)
            .filter(Chat.user_id == current_user.id)
            .order_by(Chat.criado_em.desc())
            .all()
        )
        return {"status": "success", "count": len(chats), "data": chats}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@app.delete("/finance-ai/chats")
def clear_chats(current_user: AuthUser = Depends(get_current_user)):  # noqa: B008
    db = SessionLocal()
    try:
        chat_tokens = [
            token
            for (token,) in db.query(Chat.token)
            .filter(Chat.user_id == current_user.id)
            .all()
        ]
        if chat_tokens:
            db.query(Message).filter(Message.chat_token.in_(chat_tokens)).delete(
                synchronize_session=False
            )
        deleted = (
            db.query(Chat)
            .filter(Chat.user_id == current_user.id)
            .delete(synchronize_session=False)
        )
        db.commit()
        return {"status": "success", "deleted": deleted}
    finally:
        db.close()


@app.get("/finance-ai/messages")
def get_messages(
    chat_token: str, current_user: AuthUser = Depends(get_current_user)  # noqa: B008
):
    db = SessionLocal()
    try:
        chat = (
            db.query(Chat)
            .filter(Chat.token == chat_token, Chat.user_id == current_user.id)
            .first()
        )
        if not chat:
            raise HTTPException(status_code=404, detail="Chat não encontrado.")
        messages = (
            db.query(Message)
            .filter(Message.chat_token == chat_token)
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
