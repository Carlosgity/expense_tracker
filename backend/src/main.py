### backend/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.expense_routes import router as expense_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expense_router, prefix="/api/expenses")