import { updateTodoAPI } from '@/api/endpoints/todos.api'
import type { Todo, TodoUpdate } from '@/domain/models/todo.model'
import { useMutation, useQueryClient } from '@tanstack/vue-query'

interface UpdateTodoPayload extends Partial<Omit<TodoUpdate, 'id'>> {
  id: string
}

export function useUpdateTodo() {
  const queryClient = useQueryClient()

  return useMutation<Todo, Error, UpdateTodoPayload>({
    mutationFn: (todoData) => updateTodoAPI(todoData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })
}
