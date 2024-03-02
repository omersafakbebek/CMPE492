FROM --platform=linux/amd64 node:18-alpine as base
WORKDIR /app
COPY package.json /app
COPY package-lock.json /app
RUN npm install
COPY . /app

FROM base as dev
CMD npm run start:dev

FROM base as test
RUN npm run build
ENV NODE_ENV=test
RUN npm install --only=production && npm cache clean --force
CMD npm run start:prod

FROM base as prod
RUN npm run build
ENV NODE_ENV=production
RUN npm install --only=production && npm cache clean --force
CMD npm run start:prod
