import type { TodoDto } from '@/validators/todo.validator'
import type { Todo } from '@/domain/models/todo.model'

export const mapTodoDtoToDomain = (dto: TodoDto): Todo => ({
  id: dto.id,
  title: dto.title,
  description: dto.description,
  priority: dto.priority,
  completed: dto.completed,
})

export const mapTodosDtoToDomain = (dtos: TodoDto[]): Todo[] => dtos.map(mapTodoDtoToDomain)
