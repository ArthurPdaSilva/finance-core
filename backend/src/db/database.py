from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.secrets import Secrets
from models.finance_models import Base

database_url = Secrets.DATABASE_URL or "sqlite:///app.db"
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Banco app.db criado!")
