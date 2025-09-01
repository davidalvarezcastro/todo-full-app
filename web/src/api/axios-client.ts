import { config } from '@/config'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { refreshToken } from './endpoints/auth'

declare module 'axios' {
  export interface AxiosRequestConfig {
    authRequired?: boolean
  }
}

export const apiClient = axios.create({
  baseURL: `${config.API_HOST}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
})

apiClient.interceptors.request.use((config) => {
  const auth = useAuthStore()

  if (config.authRequired !== false) {
    if (!auth.token) {
      throw new Error('No authentication token found')
    }
    config.headers.Authorization = `Bearer ${auth.token}`
  }

  return config
})

// Handle expired token (401) → try refresh
let isRefreshing = false
let failedQueue: Array<(token: string) => void> = []

const processQueue = (token: string | null) => {
  failedQueue.forEach((cb) => cb(token!))
  failedQueue = []
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const authStore = useAuthStore()

    // If 401 (Unauthorized) and not already retrying
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          failedQueue.push((token: string) => {
            originalRequest.headers['Authorization'] = `Bearer ${token}`
            resolve(apiClient(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const data = await refreshToken()
        authStore.setAuth(data)

        processQueue(data.token)
        originalRequest.headers['Authorization'] = `Bearer ${data.token}`
        return apiClient(originalRequest)
      } catch (err) {
        processQueue(null)
        authStore.logout()
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  },
)
