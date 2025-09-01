// composables/mutations/useDeleteTodo.ts
import { deleteTodo } from '@/api/endpoints/todos.api'
import { useMutation, useQueryClient } from '@tanstack/vue-query'

export function useDeleteTodo() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
    onError: (error) => {
      throw error
    },
  })
}
