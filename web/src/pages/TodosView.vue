<script setup lang="ts">
import { useTodosQuery } from '@/composables/queries/useTodosQuery'
import { ref, computed } from 'vue'

const page = ref(1)
const itemsPerPage = ref(12)

// Llamada a la query
const { data, isPending, isError, error } = useTodosQuery({
  page: page,
  items: itemsPerPage,
})

// Paginación
const totalPages = computed(() => {
  return data.value?.total_items ? Math.ceil(data.value.total_items / itemsPerPage.value) : 1
})

const nextPage = () => {
  if (data.value && data.value.page < totalPages.value) {
    page.value++
  }
}

const prevPage = () => {
  if (page.value > 1) {
    page.value--
  }
}
</script>

<template>
  <div class="min-h-screen p-6 bg-base-200 text-base-content transition-colors">
    <div class="max-w-4xl mx-auto">
      <!-- Loading -->
      <div v-if="isPending" class="alert alert-info shadow-lg mb-4">
        <span>Loading todos...</span>
      </div>

      <!-- Error -->
      <div v-if="isError" class="alert alert-error shadow-lg mb-4">
        <span>{{ error?.message || 'Failed to load todos' }}</span>
      </div>

      <div v-if="data">
        <!-- Table -->
        <div class="overflow-x-auto shadow rounded-lg">
          <table class="table w-full">
            <thead>
              <tr>
                <th>#</th>
                <th>Title</th>
                <th>Description</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(todo, index) in data.todos"
                :key="todo.id"
                :class="todo.completed ? 'bg-success/20' : 'bg-warning/20'"
              >
                <td>{{ index + 1 + (page - 1) * itemsPerPage }}</td>
                <td>{{ todo.title }}</td>
                <td>{{ todo.description }}</td>
                <td class="flex items-center gap-2 font-semibold">
                  <span>
                    <svg
                      v-if="todo.completed"
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 text-success"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                    <svg
                      v-else
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 text-warning animate-pulse"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3" />
                      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" />
                    </svg>
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between mt-4 items-center">
          <button class="btn btn-outline" :disabled="page === 1" @click="prevPage">Previous</button>
          <span class="font-medium">Page {{ page }} / {{ totalPages }}</span>
          <button class="btn btn-outline" :disabled="page === totalPages" @click="nextPage">
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
