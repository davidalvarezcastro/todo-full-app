import { z } from 'zod'

export const TodoDtoSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  priority: z.number(),
  completed: z.boolean(),
})

export const GetTodosResponseSchema = z.object({
  page: z.number(),
  total_items: z.number(),
  page_items: z.number(),
  items: z.array(TodoDtoSchema),
})

export const TodoArraySchema = z.array(TodoDtoSchema)

export type TodoDto = z.infer<typeof TodoDtoSchema>

export type GetTodosResponse = z.infer<typeof GetTodosResponseSchema>
