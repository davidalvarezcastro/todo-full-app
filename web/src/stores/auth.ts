import type { LoginResponse } from '@/api/endpoints/auth'
import Cookies from 'js-cookie'
import { defineStore } from 'pinia'

const ACCESS_TOKEN_COOKIE = 'access_token'
const EXPIRES_AT_COOKIE = 'expires_at'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: Cookies.get(ACCESS_TOKEN_COOKIE) || null,
    expiresAt: Cookies.get(EXPIRES_AT_COOKIE) || null,
  }),

  getters: {
    isTokenExpired: (state) => {
      if (!state.expiresAt) return true
      return new Date(state.expiresAt).getTime() < Date.now()
    },
    isAuthenticated: (state) => !!state.token && !useAuthStore().isTokenExpired,
  },

  actions: {
    setAuth(data: LoginResponse) {
      this.token = data.token
      this.expiresAt = data.token_expiration_date

      Cookies.set(ACCESS_TOKEN_COOKIE, data.token, {
        expires: new Date(data.token_expiration_date),
        sameSite: 'Strict',
      })

      Cookies.set(EXPIRES_AT_COOKIE, data.token_expiration_date, {
        expires: new Date(data.token_expiration_date),
        sameSite: 'Strict',
      })
    },

    loadAuth() {
      const token = Cookies.get(ACCESS_TOKEN_COOKIE)
      const expiresAt = Cookies.get(EXPIRES_AT_COOKIE)
      if (token && expiresAt) {
        this.token = token
        this.expiresAt = expiresAt
      }
    },

    logout() {
      this.token = null
      this.expiresAt = null
      Cookies.remove(ACCESS_TOKEN_COOKIE)
      Cookies.remove(EXPIRES_AT_COOKIE)
    },
  },
})
