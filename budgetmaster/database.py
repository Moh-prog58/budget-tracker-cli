from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# THIS LINE WAS MISSING — THIS IS WHY TABLES WERE NEVER CREATED
from budgetmaster.models.base import BaseModel
from budgetmaster.models.category import Category
from budgetmaster.models.transaction import Transaction
from budgetmaster.models.budget import Budget

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")  # Optional: confirmation
