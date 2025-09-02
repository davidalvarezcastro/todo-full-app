const BASE_URL = import.meta.env.VITE_API_HOSTNAME || window.location.hostname
const BASE_PORT = import.meta.env.VITE_API_PORT || 5000

const API_HOST = `${window.location.protocol}//${BASE_URL}:${BASE_PORT}`

interface AppConfig {
  API_HOST: string
}

export const config: AppConfig = {
  API_HOST: API_HOST,
}
