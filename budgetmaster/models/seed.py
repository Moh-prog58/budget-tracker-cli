from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from .category import Category
from .transaction import Transaction
from .budget import Budget

def seed_data(db: Session):
    # REMOVED: No more delete() — just add fresh data
    # This avoids "no such table" error completely

    # Create categories
    salary = Category(name="Salary", is_income=True)
    groceries = Category(name="Groceries", is_income=False)
    rent = Category(name="Rent", is_income=False)
    entertainment = Category(name="Entertainment", is_income=False)
    db.add_all([salary, groceries, rent, entertainment])
    db.commit()

    # Add transactions using relationship
    db.add_all([
        Transaction(amount=Decimal('3000.00'), description="December salary", date=date(2025, 12, 1), category=salary),
        Transaction(amount=Decimal('-180.75'), description="Supermarket", date=date(2025, 12, 4), category=groceries),
        Transaction(amount=Decimal('-1200.00'), description="Monthly rent", date=date(2025, 12, 1), category=rent),
        Transaction(amount=Decimal('-65.00'), description="Movies & dinner", date=date(2025, 12, 8), category=entertainment),
    ])

    # Add budgets
    db.add_all([
        Budget(month=12, year=2025, amount=Decimal('600.00'), category=groceries),
        Budget(month=12, year=2025, amount=Decimal('1500.00'), category=rent),
        Budget(month=12, year=2025, amount=Decimal('200.00'), category=entertainment),
    ])

    db.commit()
    print("Sample data seeded successfully!")
