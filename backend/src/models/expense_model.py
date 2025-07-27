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