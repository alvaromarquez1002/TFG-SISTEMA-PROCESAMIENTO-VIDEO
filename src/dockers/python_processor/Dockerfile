# Usamos una imagen oficial
FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# --- INSTALACIÓN DE DEPENDENCIAS ---
# 1. Actualizamos los repositorios
RUN apt-get update

# 2. Instalamos el paquete de Java por defecto
RUN apt-get install -y default-jre-headless && apt-get clean

# 3. Copiamos el archivo de requisitos de Python
COPY requirements.txt ./

# 4. Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
# Copiamos el código de nuestro script
COPY main.py .

# El comando que se ejecutará cuando el contenedor arranque
CMD ["python", "main.py"]