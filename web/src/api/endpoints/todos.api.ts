import { apiClient } from '../axios-client'
import { GetTodosResponseSchema, type GetTodosResponse } from '@/validators/todo.validator'
import type { Todo } from '@/domain/models/todo.model'
import { mapTodosDtoToDomain } from '@/domain/mappers/todo.mapper'

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
