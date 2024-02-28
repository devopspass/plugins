FROM node:20-alpine

RUN apk add --no-cache \
    make \
    gcc \
    g++ \
    python3 \
    pkgconfig \
    pixman-dev \
    cairo-dev \
    pango-dev \
    libjpeg-turbo-dev \
    giflib-dev

USER node
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

CMD ["node", "index.js"]
