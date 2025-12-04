from decimal import Decimal
from sqlalchemy import Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel

class Budget(BaseModel):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column()
    year: Mapped[int] = mapped_column()
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="budgets")

    __table_args__ = (
        UniqueConstraint('month', 'year', 'category_id', name='unique_budget_per_month'),
    )

    def __repr__(self):
        return f"<Budget {self.category.name} {self.month}/{self.year}: {self.amount}>"
