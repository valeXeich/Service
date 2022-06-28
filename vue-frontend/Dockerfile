FROM node:current-alpine

WORKDIR /app

COPY vue-frontend/package*.json ./

RUN npm install

COPY vue-frontend .

RUN npm run build

EXPOSE 8080
CMD npm run serve