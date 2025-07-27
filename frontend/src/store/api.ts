// frontend/src/store/api.ts
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
