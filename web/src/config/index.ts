interface AppConfig {
  API_HOST: string
}

export const config: AppConfig = {
  API_HOST: import.meta.env.VITE_API_HOST,
}
