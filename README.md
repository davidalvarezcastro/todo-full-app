# Todo APP

A **To-Do Web App** featuring a FastAPI back-end and a Vue-based front-end, containerized and orchestrated with Docker Compose.

---

## Overview

This project provides a full-stack template for:

- Building a RESTful API with **FastAPI** (Python).
- Creating a responsive UI using **Vue.js** (TypeScript).
- Managing dependencies and environments via **Docker Compose**.
- Accelerating development with convenient tooling such as **Makefile** and `.env` templates.

---

## Project

- **FastAPI backend** for defining robust REST endpoints. [More info](https://github.com/davidalvarezcastro/todo-full-app/tree/main/backend)
- **Vue front-end** for creating, editing, and deleting to-do items. [More info](https://github.com/davidalvarezcastro/todo-full-app/tree/main/web)

---

## Getting Started

### 1. Clone the repository

```bash
$  git clone https://github.com/davidalvarezcastro/todo-full-app.git
$  cd todo-full-app
```

### 2. Create your environment file

```bash
$ cp .env_template .env
$ cd ./backend/ && cp .env_template .env
```

### 3. Launch services (dev mode)

```bash
$ make dev
```

### 4. Access the application

- **Web APP:** http://localhost:5174
- **Fast API Docs:** http://localhost:8086/docs

---

## Pending Tasks

- [ ] Web app tests (unit + e2e)
- [ ] CI/CD deployment pipeline
