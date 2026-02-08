import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker

from models.finance_models import Base

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Banco app.db criado!")
