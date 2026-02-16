from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.secrets import Secrets
from models.finance_models import Base

engine = create_engine(Secrets.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Banco app.db criado!")
