import type { UseQueryOptions } from '@tanstack/vue-query'

export function defaultQueryOptions<TData, TError = Error>({
  enabled = true,
  staleTime = 1000 * 60 * 5, // cache 5 minutes
  retry = 3,
}: {
  enabled: boolean
  staleTime?: number
  retry?: number
}): Partial<UseQueryOptions<TData, TError>> {
  return {
    staleTime: staleTime,
    retry: retry,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    enabled,
  }
}
