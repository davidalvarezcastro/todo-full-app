# Todo App

![Vue 3](https://img.shields.io/badge/Vue%203-35495E?logo=vue.js&logoColor=4FC08D)
![Vue Router](https://img.shields.io/badge/Vue%20Router-35495E?logo=vue.js&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-FFD859?logo=vue.js&logoColor=black)
![Vue Query](https://img.shields.io/badge/Vue%20Query-FF4154?logo=reactquery&logoColor=white)
![VueUse](https://img.shields.io/badge/VueUse-42b883?logo=vue.js&logoColor=white)
![Zod](https://img.shields.io/badge/Zod-3068B7?logo=zod&logoColor=white)
![DaisyUI](https://img.shields.io/badge/DaisyUI-5A0EF8?logo=daisyui&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)

Todo Web App

## Tech Stack

- [Vue 3](https://vuejs.org/) - Frontend framework
- [Vue Router](https://router.vuejs.org/) - Client-side routing
- [Pinia](https://pinia.vuejs.org/) - State management
- [Vue Query](https://tanstack.com/query/latest/docs/vue/overview) - Data fetching & caching
- [VueUse](https://vueuse.org/) - Collection of Vue composition utilities
- [Zod](https://zod.dev/) - Schema validation
- [DaisyUI](https://daisyui.com/) - Tailwind CSS component library
- [Vite](https://vitejs.dev/) - Build tool
- [TypeScript](https://www.typescriptlang.org/) - Type safety

## Project Setup

```sh
pnpm install
```

### Compile and Hot-Reload for Development

```sh
pnpm dev
```

### Type-Check, Compile and Minify for Production

```sh
pnpm build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
pnpm test:unit
```

### Run End-to-End Tests with [Playwright](https://playwright.dev)

```sh
# Install browsers for the first run
npx playwright install

# When testing on CI, must build the project first
pnpm build

# Runs the end-to-end tests
pnpm test:e2e
# Runs the tests only on Chromium
pnpm test:e2e --project=chromium
# Runs the tests of a specific file
pnpm test:e2e tests/example.spec.ts
# Runs the tests in debug mode
pnpm test:e2e --debug
```

### Lint with [ESLint](https://eslint.org/)

```sh
pnpm lint
```
