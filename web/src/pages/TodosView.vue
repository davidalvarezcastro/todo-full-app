<script setup lang="ts">
import { ref, computed } from 'vue'
import TodoTable from '@/components/TodoTable.vue'
import TodoFormManager from '@/components/TodoFormManager.vue'
import type { Todo, TodoCreate, TodoUpdate } from '@/domain/models/todo.model'
import { useTodosQuery } from '@/composables/queries/useTodosQuery'
import { useDeleteTodo } from '@/composables/mutations/useDeleteTodo'
import { useCreateTodo } from '@/composables/mutations/useCreateTodo'
import { useUpdateTodo } from '@/composables/mutations/useUpdateTodo'

const page = ref(1)
const itemsPerPage = ref(10)
const showModal = ref(false)
const editingTodo = ref<Todo | null>(null)

// Query & Mutations
const { data, isPending, isError, error } = useTodosQuery({ page, items: itemsPerPage })
const deleteTodoMutation = useDeleteTodo()
const createMutation = useCreateTodo()
const updateMutation = useUpdateTodo()

// Pagination
const totalPages = computed(() =>
  data.value?.total_items ? Math.ceil(data.value.total_items / itemsPerPage.value) : 1,
)

const nextPage = () => {
  if (page.value < totalPages.value) page.value++
}
const prevPage = () => {
  if (page.value > 1) page.value--
}

const handleDelete = (id: string) => {
  if (confirm('Are you sure you want to delete this todo?')) {
    deleteTodoMutation.mutate({ todo: id })
  }
}

const handleCreateTodo = (todo: TodoCreate, cb: () => void) => {
  createMutation.mutate(todo, {
    onSuccess: () => {
      cb()
      closeModal()
    },
  })
}

const handleUpdateTodo = (todo: TodoUpdate, cb: () => void) => {
  updateMutation.mutate(todo, {
    onSuccess: () => {
      cb()
      closeModal()
    },
  })
}

const openCreateModal = () => {
  editingTodo.value = null
  showModal.value = true
}
const openEditModal = (todo: Todo) => {
  editingTodo.value = todo
  showModal.value = true
}
const closeModal = () => {
  showModal.value = false
  editingTodo.value = null
}
</script>

<template>
  <div class="min-h-screen p-6 bg-base-200 text-base-content transition-colors">
    <div class="max-w-4xl mx-auto">
      <div class="flex justify-end mb-4">
        <button class="btn btn-info" @click="openCreateModal">New Todo</button>
      </div>

      <div v-if="isPending" class="alert alert-info shadow-lg mb-4">
        <span>Loading todos...</span>
      </div>
      <div v-if="isError" class="alert alert-error shadow-lg mb-4">
        <span>{{ error?.message || 'Failed to load todos' }}</span>
      </div>

      <div v-if="data">
        <TodoTable
          :todos="data.todos"
          :page="page"
          :totalPages="totalPages"
          :deletePending="deleteTodoMutation.isPending.value"
          @delete="handleDelete"
          @edit="openEditModal"
          @prev-page="prevPage"
          @next-page="nextPage"
        />
      </div>

      <!-- Modal -->
      <input type="checkbox" id="todo-modal" class="modal-toggle" v-model="showModal" />
      <div class="modal">
        <div class="modal-box relative">
          <button class="btn btn-sm btn-circle absolute right-2 top-2" @click="closeModal">
            ✕
          </button>
          <TodoFormManager
            :todo="editingTodo"
            @create="handleCreateTodo"
            @update="handleUpdateTodo"
          />
        </div>
      </div>
    </div>
  </div>
</template>
