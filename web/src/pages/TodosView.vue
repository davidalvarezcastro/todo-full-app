<script setup lang="ts">
import { useDeleteTodo } from '@/composables/mutations/useDeleteTodo'
import { useTodosQuery } from '@/composables/queries/useTodosQuery'
import { ref, computed } from 'vue'

const page = ref(1)
const itemsPerPage = ref(12)

// Query & Mutations
const { data, isPending, isError, error } = useTodosQuery({
  page: page,
  items: itemsPerPage,
})

const deleteTodoMutation = useDeleteTodo()

// Pagination
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

const handleDelete = (id: string) => {
  if (confirm('Are you sure you want to delete this todo?')) {
    deleteTodoMutation.mutate({ todo: id })
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
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(todo, index) in data.todos"
                :key="todo.id"
                :class="todo.completed ? 'bg-success/25' : 'bg-warning/5'"
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

                <!-- Actions column -->
                <td>
                  <button
                    class="btn btn-square btn-error btn-sm"
                    :disabled="deleteTodoMutation.isPending.value"
                    @click="handleDelete(todo.id)"
                  >
                    <svg
                      v-if="!deleteTodoMutation.isPending.value"
                      class="w-4 h-4"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M8.586 2.586A2 2 0 0 1 10 2h4a2 2 0 0 1 2 2v2h3a1 1 0 1 1 0 2v12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V8a1 1 0 0 1 0-2h3V4a2 2 0 0 1 .586-1.414ZM10 6h4V4h-4v2Zm1 4a1 1 0 1 0-2 0v8a1 1 0 1 0 2 0v-8Zm4 0a1 1 0 1 0-2 0v8a1 1 0 1 0 2 0v-8Z"
                        clip-rule="evenodd"
                      />
                    </svg>

                    <span v-else class="loading loading-spinner"></span>
                  </button>
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
