import { apiClient } from '../axios-client'
import { GetTodosResponseSchema, type GetTodosResponse } from '@/validators/todo.validator'
import type { Todo, TodoCreate, TodoUpdate } from '@/domain/models/todo.model'
import { mapTodoDtoToDomain, mapTodosDtoToDomain } from '@/domain/mappers/todo.mapper'

export interface PaginationTodos {
  page: number
  total_items: number
  page_items: number
  todos: Todo[]
}

export const getTodos = async ({
  page,
  items,
}: {
  page: number
  items: number
}): Promise<PaginationTodos> => {
  try {
    const { data } = await apiClient.post<GetTodosResponse>('/todos', { page, items })

    const parsed = GetTodosResponseSchema.parse(data)

    return {
      page: parsed.page,
      total_items: parsed.total_items,
      page_items: parsed.page_items,
      todos: mapTodosDtoToDomain(parsed.items),
    }
  } catch (error) {
    throw error
  }
}

export const deleteTodo = async ({ todo }: { todo: string }): Promise<void> => {
  try {
    await apiClient.delete<GetTodosResponse>(`/todo/${todo}`)
  } catch (error) {
    throw error
  }
}

export const createTodoAPI = async (todo: TodoCreate): Promise<void> => {
  try {
    await apiClient.post('/todo', todo)
  } catch (error) {
    throw error
  }
}

export const updateTodoAPI = async (todo: TodoUpdate): Promise<Todo> => {
  try {
    const { data } = await apiClient.put(`/todo/${todo.id}`, todo)

    return mapTodoDtoToDomain(data)
  } catch (error) {
    throw error
  }
}
