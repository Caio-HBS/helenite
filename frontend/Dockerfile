FROM node:latest

WORKDIR /app

COPY ./frontend/package.json /app/

RUN npm install

COPY ./frontend .

CMD ["npm", "run", "dev"]
