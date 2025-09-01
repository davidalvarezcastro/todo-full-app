export interface Todo {
  id: string
  title: string
  description: string
  priority: number
  completed: boolean
}

export type TodoCreate = Pick<Todo, 'title' | 'description' | 'priority'>

export interface TodoUpdate {
  id: string
  description?: string
  priority?: number
  completed?: boolean
}
