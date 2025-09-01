<script setup lang="ts">
import { computed, ref } from 'vue'
import { useLogin } from '@/composables/mutations/useAuth'
import type { AxiosError } from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const showPassword = ref(false)

const router = useRouter()

const loginMutation = useLogin()

const doLogin = async () => {
  try {
    await loginMutation.mutateAsync({ email: email.value, password: password.value })
    router.push({ name: 'Home' })
    // eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars
  } catch (err: any) {
    // TODO: notification message
  }
}

const errorMessage = computed(() => {
  const err = loginMutation.error.value as AxiosError | null
  return err?.message ?? 'Login failed'
})
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200">
    <div class="card w-full max-w-sm shadow-xl bg-base-100">
      <div class="card-body">
        <h2 class="card-title text-center text-2xl font-bold mb-4">Login</h2>

        <!-- Email -->
        <div class="form-control mb-3">
          <label class="label">
            <span class="label-text">Email</span>
          </label>
          <input
            type="email"
            placeholder="Enter your email"
            class="input input-bordered w-full"
            v-model="email"
            autocomplete="email"
          />
        </div>

        <!-- Password -->
        <div class="form-control mb-3 relative">
          <label class="label">
            <span class="label-text">Password</span>
          </label>
          <input
            :type="showPassword ? 'text' : 'password'"
            placeholder="Enter your password"
            class="input input-bordered w-full pr-10"
            v-model="password"
          />

          <label
            class="swap swap-rotate absolute right-4 top-10 -translate-y-1/2 cursor-pointer z-50"
          >
            <input type="checkbox" v-model="showPassword" />

            <!-- Eye closed -->
            <svg
              class="swap-off w-6 h-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                fill-rule="evenodd"
                d="M4.998 7.78C6.729 6.345 9.198 5 12 5c2.802 0 5.27 1.345 7.002 2.78a12.713 12.713 0 0 1 2.096 2.183c.253.344.465.682.618.997.14.286.284.658.284 1.04s-.145.754-.284 1.04a6.6 6.6 0 0 1-.618.997 12.712 12.712 0 0 1-2.096 2.183C17.271 17.655 14.802 19 12 19c-2.802 0-5.27-1.345-7.002-2.78a12.712 12.712 0 0 1-2.096-2.183 6.6 6.6 0 0 1-.618-.997C2.144 12.754 2 12.382 2 12s.145-.754.284-1.04c.153-.315.365-.653.618-.997A12.714 12.714 0 0 1 4.998 7.78ZM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"
                clip-rule="evenodd"
              />
            </svg>

            <!-- Eye open -->
            <svg
              class="swap-on w-6 h-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                d="m4 15.6 3.055-3.056A4.913 4.913 0 0 1 7 12.012a5.006 5.006 0 0 1 5-5c.178.009.356.027.532.054l1.744-1.744A8.973 8.973 0 0 0 12 5.012c-5.388 0-10 5.336-10 7A6.49 6.49 0 0 0 4 15.6Z"
              />
              <path
                d="m14.7 10.726 4.995-5.007A.998.998 0 0 0 18.99 4a1 1 0 0 0-.71.305l-4.995 5.007a2.98 2.98 0 0 0-.588-.21l-.035-.01a2.981 2.981 0 0 0-3.584 3.583c0 .012.008.022.01.033.05.204.12.402.211.59l-4.995 4.983a1 1 0 1 0 1.414 1.414l4.995-4.983c.189.091.386.162.59.211.011 0 .021.007.033.01a2.982 2.982 0 0 0 3.584-3.584c0-.012-.008-.023-.011-.035a3.05 3.05 0 0 0-.21-.588Z"
              />
              <path
                d="m19.821 8.605-2.857 2.857a4.952 4.952 0 0 1-5.514 5.514l-1.785 1.785c.767.166 1.55.25 2.335.251 6.453 0 10-5.258 10-7 0-1.166-1.637-2.874-2.179-3.407Z"
              />
            </svg>
          </label>
        </div>

        <!-- Button -->
        <div class="form-control mt-6 text-right">
          <button
            class="btn btn-success"
            :class="{ 'btn-disabled': loginMutation.isPending.value }"
            @click="doLogin"
          >
            <span v-if="loginMutation.isPending.value" class="loading loading-spinner"></span>
            <span v-else>Login</span>
          </button>
        </div>

        <!-- Error -->
        <p v-if="loginMutation.isError.value" class="text-error mt-2 text-center">
          {{ errorMessage }}
        </p>
      </div>
    </div>
  </div>
</template>
