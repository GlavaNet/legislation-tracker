# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 3000

ENV VITE_API_URL=http://localhost:8000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
