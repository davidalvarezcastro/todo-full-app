<script setup lang="ts">
import { ref, watch, computed, defineProps, defineEmits } from 'vue'
import type { Todo } from '@/domain/models/todo.model'

interface Props {
  todo?: Todo | null
  title: string
  description: string
  priority: number
  completed: boolean
  pending: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (event: 'update:title', value: string): void
  (event: 'update:description', value: string): void
  (event: 'update:priority', value: number): void
  (event: 'update:completed', value: boolean): void
  (event: 'submit'): void
}>()

const MAX_PRIORITY = 10
const isEditing = computed(() => !!props.todo)

// Refs internos
const titleInternal = ref(props.title)
const descriptionInternal = ref(props.description)
const priorityInternal = ref(props.priority)
const completedInternal = ref(props.completed)

// Sincronizar cambios de props
watch(
  () => props.title,
  (val) => (titleInternal.value = val),
)
watch(
  () => props.description,
  (val) => (descriptionInternal.value = val),
)
watch(
  () => props.priority,
  (val) => (priorityInternal.value = val),
)
watch(
  () => props.completed,
  (val) => (completedInternal.value = val),
)

// Funciones de manejo de eventos tipadas
const updateTitleEvent = (event: Event) => {
  const target = event.currentTarget as HTMLInputElement
  titleInternal.value = target.value
  emit('update:title', target.value)
}

const updateDescriptionEvent = (event: Event) => {
  const target = event.currentTarget as HTMLTextAreaElement
  descriptionInternal.value = target.value
  emit('update:description', target.value)
}

const updatePriorityEvent = (p: number) => {
  priorityInternal.value = p
  emit('update:priority', p)
}

const updateCompletedEvent = (event: Event) => {
  const target = event.currentTarget as HTMLInputElement
  completedInternal.value = target.checked
  emit('update:completed', target.checked)
}
</script>

<template>
  <div class="bg-base-100 p-2">
    <h2 class="text-xl font-bold mb-4">{{ isEditing ? `Edit ${props.todo?.id}` : 'New Todo' }}</h2>

    <div class="form-control mb-3">
      <label class="label"><span class="label-text">Title</span></label>
      <input
        v-model="titleInternal"
        type="text"
        placeholder="Title"
        class="input input-bordered w-full"
        :disabled="isEditing"
        @input="updateTitleEvent"
      />
    </div>

    <div class="form-control mb-3">
      <label class="label"><span class="label-text">Description</span></label>
      <textarea
        v-model="descriptionInternal"
        class="textarea textarea-bordered w-full"
        placeholder="Description"
        @input="updateDescriptionEvent"
      ></textarea>
    </div>

    <div class="form-control mb-3">
      <label class="label"><span class="label-text">Priority</span></label>
      <div class="flex gap-2">
        <button
          v-for="p in MAX_PRIORITY"
          :key="p"
          type="button"
          @click="updatePriorityEvent(p)"
          :class="['btn btn-sm', priorityInternal === p ? 'btn-info' : 'btn-outline']"
        >
          {{ p }}
        </button>
      </div>
    </div>

    <div v-if="isEditing" class="form-control mb-3 flex items-center gap-2">
      <input
        type="checkbox"
        :checked="completedInternal"
        class="checkbox"
        @change="updateCompletedEvent"
      />
      <span>Completed</span>
    </div>

    <div class="form-control mt-4 text-right">
      <button
        class="btn btn-success"
        :class="{ 'btn-disabled': props.pending }"
        @click="$emit('submit')"
      >
        <span v-if="props.pending" class="loading loading-spinner"></span>
        <span v-else>{{ isEditing ? 'Update' : 'Create' }}</span>
      </button>
    </div>
  </div>
</template>
