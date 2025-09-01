import { useMutation } from '@tanstack/vue-query'
import {
  login,
  refreshToken as refreshTokenAPI,
  type LoginRequest,
  type LoginResponse,
} from '@/api/endpoints/auth'
import { useAuthStore } from '@/stores/auth'
import type { AxiosError } from 'axios'

export function useLogin() {
  const authStore = useAuthStore()

  return useMutation<LoginResponse, AxiosError, LoginRequest>({
    mutationFn: (data) => login(data),
    onSuccess: (data) => {
      authStore.setAuth(data)
    },
  })
}

export function useRefreshToken() {
  const authStore = useAuthStore()

  return useMutation<LoginResponse, Error, void>({
    mutationFn: () => refreshTokenAPI(),
    onSuccess: (data) => {
      authStore.setAuth(data)
    },
    onError: () => {
      authStore.logout()
    },
  })
}
