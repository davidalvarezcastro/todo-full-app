<script setup lang="ts">
import { ref, watch, computed, defineProps, defineEmits } from 'vue'
import type { Todo, TodoCreate, TodoUpdate } from '@/domain/models/todo.model'

interface Props {
  todo?: Todo | null
}

const MAX_PRIORITY = 10

const props = defineProps<Props>()
const emit = defineEmits<{
  (event: 'create', todo: TodoCreate, cb: () => void): void
  (event: 'update', todo: TodoUpdate, cb: () => void): void
}>()

const pending = ref(false)

const title = ref(props.todo?.title || '')
const description = ref(props.todo?.description || '')
const priority = ref(props.todo?.priority || 1)
const completed = ref(props.todo?.completed || false)

watch(
  () => props.todo,
  (newTodo) => {
    if (newTodo) {
      title.value = newTodo.title
      description.value = newTodo.description
      priority.value = newTodo.priority
      completed.value = newTodo.completed
    } else {
      title.value = ''
      description.value = ''
      priority.value = 1
      completed.value = false
    }
  },
)

// Mutations

const isEditing = computed(() => !!props.todo)

const handleSubmit = () => {
  if (isEditing.value && props.todo) {
    emit(
      'update',
      {
        id: props.todo.id,
        description: description.value,
        priority: priority.value,
        completed: completed.value,
      },
      () => {
        pending.value = false
      },
    )
  } else {
    emit(
      'create',
      {
        title: title.value,
        description: description.value,
        priority: priority.value,
      },
      () => {
        pending.value = false
      },
    )
  }
}
</script>

<template>
  <div class="bg-base-100 p-2">
    <h2 class="text-xl font-bold mb-4">{{ isEditing ? `Edit ${todo?.id}` : 'New Todo' }}</h2>

    <div class="form-control mb-3">
      <label class="label"><span class="label-text">Title</span></label>
      <input
        v-model="title"
        type="text"
        placeholder="Title"
        class="input input-bordered w-full"
        :disabled="isEditing"
      />
    </div>

    <div class="form-control mb-3">
      <label class="label"><span class="label-text">Description</span></label>
      <textarea
        v-model="description"
        class="textarea textarea-bordered w-full"
        placeholder="Description"
      ></textarea>
    </div>

    <div class="form-control mb-3">
      <label class="label"><span class="label-text">Priority</span></label>
      <div class="flex gap-2">
        <button
          v-for="p in MAX_PRIORITY"
          :key="p"
          type="button"
          @click="priority = p"
          :class="['btn btn-sm', priority === p ? 'btn-info' : 'btn-outline']"
        >
          {{ p }}
        </button>
      </div>
    </div>

    <div v-if="isEditing" class="form-control mb-3 flex items-center gap-2">
      <input type="checkbox" v-model="completed" class="checkbox" />
      <span>Completed</span>
    </div>

    <div class="form-control mt-4 text-right">
      <button
        class="btn btn-success"
        :class="{
          'btn-disabled': pending,
        }"
        @click="handleSubmit"
      >
        <span v-if="pending" class="loading loading-spinner"></span>
        <span v-else>{{ isEditing ? 'Update' : 'Create' }}</span>
      </button>
    </div>
  </div>
</template>
