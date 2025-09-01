<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import type { Todo } from '@/domain/models/todo.model'

interface Props {
  todos: Todo[]
  page: number
  totalPages: number
  deletePending: boolean
}

const props = defineProps<Props>()
defineEmits<{
  (event: 'delete', id: string): void
  (event: 'edit', todo: Todo): void
  (event: 'prev-page'): void
  (event: 'next-page'): void
}>()
</script>

<template>
  <div>
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
            v-for="(todo, index) in todos"
            :key="todo.id"
            :class="todo.completed ? 'bg-success/25' : 'bg-warning/5'"
          >
            <td>{{ index + 1 + (props.page - 1) * todos.length }}</td>
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
              <div class="flex justify-around">
                <button
                  class="btn btn-square btn-error btn-sm"
                  :disabled="deletePending"
                  @click="$emit('delete', todo.id)"
                >
                  <span v-if="!deletePending">
                    <svg
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
                  </span>
                  <span v-else class="loading loading-spinner"></span>
                </button>

                <button class="btn btn-square btn-accent btn-sm" @click="$emit('edit', todo)">
                  Edit
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="flex justify-between mt-4 items-center">
      <button class="btn btn-outline" :disabled="page === 1" @click="$emit('prev-page')">
        Previous
      </button>
      <span class="font-medium">Page {{ page }} / {{ totalPages }}</span>
      <button class="btn btn-outline" :disabled="page === totalPages" @click="$emit('next-page')">
        Next
      </button>
    </div>
  </div>
</template>
