# budgetmaster/models/base.py
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base   
class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

    @classmethod
    def find_by_id(cls, db, id_):
        return db.query(cls).get(id_)