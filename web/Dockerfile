FROM docker.io/node:22-slim AS base

# Variables de entorno
ENV HTTP_PROXY=http://isfman:isfman@1.0.0.70:3128
ENV HTTPS_PROXY=http://isfman:isfman@1.0.0.70:3128
ENV NO_PROXY=localhost,127.0.0.1


LABEL AUTHOR=davalv
ENV TZ=Europe/Madrid
ENV PNPM_HOME="/pnpm"  
ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable

WORKDIR /app
COPY package*.json ./
RUN pnpm install

FROM base AS dev
EXPOSE 5173
CMD ["pnpm", "run", "dev", "--host"]

FROM docker.io/node:22-slim AS build
ARG BRANCH
LABEL AUTHOR=davalv
ENV TZ=Europe/Madrid
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app
COPY ./ .
RUN pnpm install && pnpm build --mode=${BRANCH}


FROM docker.io/nginxinc/nginx-unprivileged:1.27-alpine-perl AS production
COPY nginx/ /etc/nginx/conf.d/
COPY --from=build /app/dist /srv/http/todoapp
