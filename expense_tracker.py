### backend/src/config/db.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


### backend/src/models/expense_model.py
from config.db import connect_db

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            amount NUMERIC NOT NULL,
            category VARCHAR(50),
            description TEXT,
            date DATE DEFAULT CURRENT_DATE
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_expense(amount, category, description, date):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s)",
                (amount, category, description, date))
    conn.commit()
    cur.close()
    conn.close()

def get_expenses():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    cur.close()
    conn.close()

def summarize_expenses():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


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


### backend/.env
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432


### backend/requirements.txt
fastapi
uvicorn
psycopg2-binary
python-dotenv
python-multipart


### frontend/src/store/api.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const expenseApi = createApi({
  reducerPath: 'expenseApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://localhost:8000/api/expenses' }),
  tagTypes: ['Expenses'],
  endpoints: (builder) => ({
    getExpenses: builder.query<any[], void>({
      query: () => '/',
      providesTags: ['Expenses'],
    }),
    addExpense: builder.mutation<void, any>({
      query: (expense) => ({
        url: '/',
        method: 'POST',
        body: expense,
      }),
      invalidatesTags: ['Expenses'],
    }),
    deleteExpense: builder.mutation<void, number>({
      query: (id) => ({
        url: `/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Expenses'],
    }),
    getSummary: builder.query<any[], void>({
      query: () => '/summary',
    }),
  }),
});

export const {
  useGetExpensesQuery,
  useAddExpenseMutation,
  useDeleteExpenseMutation,
  useGetSummaryQuery,
} = expenseApi;


### frontend/src/store/store.ts
import { configureStore } from '@reduxjs/toolkit';
import { expenseApi } from './api';

export const store = configureStore({
  reducer: {
    [expenseApi.reducerPath]: expenseApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(expenseApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;


### frontend/src/pages/Expenses.tsx
import { useState } from 'react';
import {
  useGetExpensesQuery,
  useAddExpenseMutation,
  useDeleteExpenseMutation,
  useGetSummaryQuery,
} from '../store/api';

export default function Expenses() {
  const { data: expenses = [] } = useGetExpensesQuery();
  const { data: summary = [] } = useGetSummaryQuery();
  const [addExpense] = useAddExpenseMutation();
  const [deleteExpense] = useDeleteExpenseMutation();

  const [form, setForm] = useState({ amount: '', category: '', description: '', date: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await addExpense({ ...form, amount: parseFloat(form.amount) });
    setForm({ amount: '', category: '', description: '', date: '' });
  };

  const handleDelete = async (id: number) => {
    await deleteExpense(id);
  };

  return (
    <div>
      <h2>Expense Tracker</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder='Amount' value={form.amount} onChange={e => setForm({ ...form, amount: e.target.value })} />
        <input placeholder='Category' value={form.category} onChange={e => setForm({ ...form, category: e.target.value })} />
        <input placeholder='Description' value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
        <input type='date' value={form.date} onChange={e => setForm({ ...form, date: e.target.value })} />
        <button type='submit'>Add</button>
      </form>

      <ul>
        {expenses.map((exp: any) => (
          <li key={exp.id}>
            ${exp.amount} | {exp.category} | {exp.description} | {exp.date}
            <button onClick={() => handleDelete(exp.id)}>Delete</button>
          </li>
        ))}
      </ul>

      <h3>Summary</h3>
      <ul>
        {summary.map((item: any, index: number) => (
          <li key={index}>{item[0]}: ${item[1]}</li>
        ))}
      </ul>
    </div>
  );
}


### frontend/src/App.tsx
import Expenses from './pages/Expenses';

function App() {
  return (
    <div className="App">
      <Expenses />
    </div>
  );
}

export default App;


### frontend/src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { Provider } from 'react-redux';
import { store } from './store/store';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);


### frontend/package.json (partial)
{
  "name": "frontend",
  "version": "0.0.1",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@reduxjs/toolkit": "^latest",
    "axios": "^latest",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-redux": "^latest"
  },
  "devDependencies": {
    "@types/react": "^18.0.27",
    "@types/react-dom": "^18.0.10",
    "typescript": "^4.9.3",
    "vite": "^4.0.0"
  }
}
