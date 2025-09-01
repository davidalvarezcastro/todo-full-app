import { createTodoAPI } from '@/api/endpoints/todos.api'
import type { TodoCreate } from '@/domain/models/todo.model'
import { useMutation, useQueryClient } from '@tanstack/vue-query'

export function useCreateTodo() {
  const queryClient = useQueryClient()

  return useMutation<void, Error, Omit<TodoCreate, 'id'>>({
    mutationFn: (todoData) => createTodoAPI(todoData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })
}
