# Usamos una imagen oficial de Python como base
FROM python:3.9-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 1. Copiamos PRIMERO el archivo de requisitos
COPY requirements.txt ./

# 2. Instalamos las dependencias listadas en el archivo
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiamos el resto del código
COPY ./process /app/process

# 4. El comando que se ejecutará cuando el contenedor arranque
CMD ["python", "./process/main.py"]