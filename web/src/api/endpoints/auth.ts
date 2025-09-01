import { apiClient } from '../axios-client'

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  token: string
  token_expiration_date: string
}

export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  try {
    const res = await apiClient.post<LoginResponse>('/auth/login', data, { authRequired: false })
    return res.data
  } catch (error) {
    throw error
  }
}

export const refreshToken = async (): Promise<{ token: string; token_expiration_date: string }> => {
  try {
    const res = await apiClient.post('/auth/refresh')
    return res.data
  } catch (error) {
    throw error
  }
}
