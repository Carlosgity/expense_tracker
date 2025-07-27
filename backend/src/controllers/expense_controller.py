### backend/src/controllers/expense_controller.py
from models.expense_model import insert_expense, get_expenses, delete_expense as delete_expense_model, summarize_expenses

def add_expense_controller(expense):
    insert_expense(expense.amount, expense.category, expense.description, expense.date)
    return {"message": "Expense added successfully"}

def get_expenses_controller():
    return get_expenses()

def delete_expense_controller(expense_id):
    delete_expense_model(expense_id)
    return {"message": "Expense deleted successfully"}

def summarize_expenses_controller():
    return summarize_expenses()