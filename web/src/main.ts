import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query'

import App from './App.vue'
import router from './router'

import './styles/index.css'

const app = createApp(App)
const pinia = createPinia()
const queryClient = new QueryClient()

app.use(pinia)
app.use(router)
app.use(VueQueryPlugin, { queryClient })

app.mount('#app')
