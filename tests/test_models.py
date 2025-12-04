import pytest
from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session
from budgetmaster.database import get_db, init_db
from budgetmaster.models.category import Category
from budgetmaster.models.transaction import Transaction
from budgetmaster.models.budget import Budget

@pytest.fixture
def db_session():
    init_db()
    db = next(get_db())
    yield db
    db.rollback()

def test_create_category(db_session: Session):
    cat = Category(name="Test", is_income=False)
    db_session.add(cat)
    db_session.commit()
    assert cat.id is not None

def test_create_transaction(db_session: Session):
    cat = Category(name="Test")
    db_session.add(cat)
    db_session.commit()
    trans = Transaction(amount=Decimal('10.00'), description="Test", category_id=cat.id, date=date(2025, 12, 4))
    db_session.add(trans)
    db_session.commit()
    assert trans.id is not None

def test_budget_unique(db_session: Session):
    cat = Category(name="Test")
    db_session.add(cat)
    db_session.commit()
    bud1 = Budget(month=12, year=2025, amount=Decimal('100.00'), category_id=cat.id)
    db_session.add(bud1)
    db_session.commit()
    with pytest.raises(Exception):  # Unique constraint
        bud2 = Budget(month=12, year=2025, amount=Decimal('200.00'), category_id=cat.id)
        db_session.add(bud2)
        db_session.commit()