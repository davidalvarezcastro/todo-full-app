import { keepPreviousData, useQuery } from '@tanstack/vue-query'
import { getTodos, type PaginationTodos } from '@/api/endpoints/todos.api'
import { defaultQueryOptions } from './useQueryDefaults'
import type { Ref } from 'vue'

interface UseTodosQueryOptions {
  page: Ref<number>
  items: Ref<number>
}

export function useTodosQuery(options: UseTodosQueryOptions) {
  const { page, items } = options

  return useQuery<PaginationTodos, Error>({
    queryKey: ['todos', page, items],
    queryFn: () => getTodos({ page: page.value, items: items.value }),
    ...defaultQueryOptions<PaginationTodos, Error>({ enabled: true }),
    placeholderData: keepPreviousData,
  })
}
