<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()

const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push({ name: 'Login' })
}
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm px-4">
    <div class="flex-1">
      <a class="btn btn-ghost text-xl">Todo App</a>
    </div>
    <div class="flex-none">
      <!-- Botón logout solo si está logueado -->
      <button v-if="authStore.isAuthenticated" @click="handleLogout" class="btn btn-outline btn-sm">
        Logout
      </button>
    </div>
  </div>

  <router-view></router-view>
</template>

<style scoped></style>
