# 1. Imagen Base: Empezamos con una imagen oficial de Python. 
#    'slim' es más ligera.
FROM python:3.13-slim

# 2. Directorio de Trabajo: Creamos una carpeta '/app' dentro de la imagen 
#    y nos situamos ahí para los siguientes comandos.
WORKDIR /app

# 3. Dependencias: Copiamos el archivo de requisitos y las instalamos.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar Código: Copiamos todo el contenido de la carpeta 'src' local 
#    (donde está este Dockerfile) a la carpeta '/app' dentro de la imagen.
COPY . .

# 5. Comando por Defecto: Qué comando se ejecutará cuando inicie un contenedor 
#    basado en esta imagen. Para empezar y probar, simplemente mostraremos 
#    la versión de Python instalada dentro del contenedor.
CMD ["python", "./main.py"]
