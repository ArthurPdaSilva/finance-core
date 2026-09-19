from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from fastapi import Header, HTTPException, status
from pwdlib import PasswordHash

from config.secrets import Secrets
from db.database import SessionLocal
from models.finance_models import AuthUser, UserSession

password_hash = PasswordHash.recommended()
current_user_id: ContextVar[int | None] = ContextVar("current_user_id", default=None)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_session(db, user: AuthUser) -> str:
    token = secrets.token_urlsafe(32)
    session = UserSession(
        user_id=user.id,
        token_hash=hash_session_token(token),
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=Secrets.SESSION_TTL_DAYS),
    )
    db.add(session)
    db.commit()
    return token


def get_session_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.removeprefix("Bearer ").strip()


def get_current_session(authorization: str | None = Header(default=None)):
    token = get_session_token(authorization)
    db = SessionLocal()
    try:
        session = (
            db.query(UserSession)
            .filter(
                UserSession.token_hash == hash_session_token(token),
                UserSession.revoked_at.is_(None),
            )
            .first()
        )
        now = datetime.now(timezone.utc)
        expires_at = session.expires_at if session else now
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if not session or expires_at <= now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sessão inválida ou expirada.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return session
    finally:
        db.close()


def get_current_user(authorization: str | None = Header(default=None)) -> AuthUser:
    session = get_current_session(authorization)
    db = SessionLocal()
    try:
        user = db.query(AuthUser).filter(AuthUser.id == session.user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado.")
        return user
    finally:
        db.close()


@contextmanager
def user_context(user_id: int):
    token = current_user_id.set(user_id)
    try:
        yield
    finally:
        current_user_id.reset(token)


def require_current_user_id() -> int:
    user_id = current_user_id.get()
    if user_id is None:
        raise RuntimeError("Usuário autenticado não encontrado no contexto da requisição.")
    return user_id
