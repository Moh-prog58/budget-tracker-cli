import click
from rich.console import Console
from rich.table import Table
from decimal import Decimal
from datetime import date
from budgetmaster.database import get_db, init_db

console = Console()

@click.group()
def cli():
    pass

@cli.command()
def seed():
    
    init_db()  
    from budgetmaster.models.seed import seed_data
    db = next(get_db())
    seed_data(db)
    console.print("Database seeded with sample data!", style="bold green")

@cli.command()
def list_categories():
    init_db()
    from budgetmaster.models.category import Category
    db = next(get_db())
    cats = db.query(Category).all()
    table = Table(title="Categories")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Type")
    for cat in cats:
        table.add_row(str(cat.id), cat.name, "Income" if cat.is_income else "Expense")
    console.print(table)

@cli.command()
@click.argument('name')
@click.option('--income', is_flag=True)
def add_category(name, income):
    init_db()
    from budgetmaster.models.category import Category
    db = next(get_db())
    cat = Category(name=name, is_income=income)
    db.add(cat)
    db.commit()
    console.print(f"Added category: {name}", style="green")

@cli.command()
@click.argument('category_name')
@click.argument('amount', type=float)
@click.argument('description', default="")
def add_transaction(category_name, amount, description):
    init_db()
    from budgetmaster.models.category import Category
    from budgetmaster.models.transaction import Transaction
    db = next(get_db())
    cat = db.query(Category).filter_by(name=category_name).first()
    if not cat:
        console.print("Category not found!", style="red")
        return
    t = Transaction(amount=Decimal(str(amount)), description=description or "No description", category=cat)
    db.add(t)
    db.commit()
    console.print(f"Added {amount} to {category_name}", style="green")

@cli.command()
@click.argument('category_name')
@click.argument('amount', type=float)
@click.option('--month', default=date.today().month)
@click.option('--year', default=date.today().year)
def budget(category_name, amount, month, year):
    init_db()
    from budgetmaster.models.category import Category
    from budgetmaster.models.budget import Budget
    db = next(get_db())
    cat = db.query(Category).filter_by(name=category_name).first()
    if not cat:
        console.print("Category not found!", style="red")
        return
    existing = db.query(Budget).filter_by(category_id=cat.id, month=month, year=year).first()
    if existing:
        existing.amount = Decimal(str(amount))
    else:
        db.add(Budget(month=month, year=year, amount=Decimal(str(amount)), category=cat))
    db.commit()
    console.print(f"Budget set: {category_name} {month}/{year} = {amount}", style="green")

@cli.command()
@click.option('--month', default=date.today().month)
@click.option('--year', default=date.today().year)
def report(month, year):
    init_db()
    from budgetmaster.models.budget import Budget
    from budgetmaster.models.transaction import Transaction
    db = next(get_db())

    table = Table(title=f"Budget Report — {month}/{year}")
    table.add_column("Category")
    table.add_column("Budget", justify="right")
    table.add_column("Spent", justify="right")
    table.add_column("Remaining", justify="right")

    budgets = db.query(Budget).filter_by(month=month, year=year).all()
    for b in budgets:
        if b.category.is_income:
            continue
        spent = abs(db.query(Transaction.amount).filter(
            Transaction.category == b.category,
            Transaction.date.between(f"{year}-{month:02d}-01", f"{year}-{month:02d}-31")
        ).scalar() or Decimal('0'))
        remaining = b.amount - spent
        style = "red" if remaining < 0 else "green"
        table.add_row(b.category.name, str(b.amount), f"{spent:.2f}", f"{remaining:.2f}", style=style)

    console.print(table)

if __name__ == "__main__":
    cli()
