from typing import List
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    is_income: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships (lists of related objects)
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="category")
    budgets: Mapped[List["Budget"]] = relationship("Budget", back_populates="category")