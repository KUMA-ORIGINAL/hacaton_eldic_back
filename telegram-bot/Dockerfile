# Используем официальный Node.js образ
FROM node:20-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install --production

# Копируем весь проект
COPY . .

# Экспорт переменной окружения (если хотите внутри контейнера)
ENV NODE_ENV=production

# Команда запуска бота
CMD ["npm", "start"]
