### backend/src/routes/expense_routes.py
from fastapi import APIRouter
from controllers.expense_controller import (
    add_expense_controller,
    get_expenses_controller,
    delete_expense_controller,
    summarize_expenses_controller
)
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class Expense(BaseModel):
    amount: float
    category: str
    description: str
    date: date

@router.post("/")
def add_expense(expense: Expense):
    return add_expense_controller(expense)

@router.get("/")
def read_expenses():
    return get_expenses_controller()

@router.delete("/{expense_id}")
def delete_expense(expense_id: int):
    return delete_expense_controller(expense_id)

@router.get("/summary")
def get_summary():
    return summarize_expenses_controller()