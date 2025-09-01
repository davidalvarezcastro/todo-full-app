<script setup lang="ts">
import { ref, watch } from 'vue'
import TodoFormUI from './TodoFormUI.vue'
import type { Todo, TodoCreate, TodoUpdate } from '@/domain/models/todo.model'

interface Props {
  todo?: Todo | null
}

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

const handleSubmit = () => {
  pending.value = true
  if (props.todo) {
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
  <TodoFormUI
    :todo="props.todo"
    :title="title"
    :description="description"
    :priority="priority"
    :completed="completed"
    :pending="pending"
    @update:title="title = $event"
    @update:description="description = $event"
    @update:priority="priority = $event"
    @update:completed="completed = $event"
    @submit="handleSubmit"
  />
</template>
