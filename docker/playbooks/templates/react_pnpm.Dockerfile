FROM node:20-alpine as build

RUN npm install -g pnpm

WORKDIR /app
COPY package*.json ./
RUN CI=true pnpm install
COPY . .
RUN pnpm build

FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
