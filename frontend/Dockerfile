# Usamos una imagen ligera de Node
FROM node:18-alpine

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos solo los archivos de dependencias primero (para aprovechar caché)
COPY package*.json ./

# Instalamos las librerías
RUN npm install

# Copiamos el resto del código
COPY . .

# Exponemos el puerto de React
EXPOSE 3000

# Arrancamos la app
# Por esto (si usas Vite):
CMD ["npm", "run", "dev", "--", "--host"]