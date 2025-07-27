// frontend/src/pages/Expenses.tsx
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