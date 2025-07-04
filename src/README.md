# Pipeline de Procesamiento de Datos (Kafka y Spark)

Este directorio contiene toda la lógica y la infraestructura para el pipeline de procesamiento de vídeo. Está diseñado para ser un sistema modular que consume los vídeos generados por Jitsi y les aplica transformaciones.

## Arquitectura del Pipeline

El sistema se basa en tres componentes principales orquestados por Docker Compose:
1.  **Apache Kafka (KRaft Mode):** Actúa como un broker de mensajería para desacoplar las fases del pipeline. Un evento se produce en Kafka cuando un nuevo vídeo está listo para ser procesado.
2.  **Apache Spark:** Un clúster simple compuesto por un `spark-master` y un `spark-worker`, que proporciona el entorno de computación distribuida para el análisis.
3.  **Python Processor:** Un servicio personalizado que contiene la lógica de la aplicación, incluyendo:
    * Un **productor** que vigila el directorio de grabaciones y envía mensajes a Kafka.
    * Un **consumidor** que lee de Kafka y envía los trabajos de procesamiento a Spark.

## Descripción de Ficheros y Directorios

* **`docker-compose.yml`**:
    * Este fichero orquesta todos los servicios del pipeline: `kafka`, `spark-master`, `spark-worker` y `python-processor`. Define la red, los volúmenes compartidos y las dependencias entre servicios.

* **`/dockers/python_processor/`**:
    * Contiene todo lo necesario para construir la imagen del servicio de Python:
        * **`Dockerfile`**: Define la imagen de Python, instala las dependencias de sistema y las librerías de Python listadas en `requirements.txt`.
        * **`main.py`**: Es el script principal de la aplicación. Contiene la lógica para conectar con Spark y realizar el procesamiento de vídeo con OpenCV.
        * **`requirements.txt`**: Lista las dependencias de Python (ej. `pyspark`, `opencv-python-headless`, `kafka-python`).

* **`/data/`**:
    * Este directorio está mapeado como un volumen de Docker. Es el punto de entrada para los vídeos que vienen de Jibri y donde se guardarán los resultados.
    * **`/data/processed/`**: Subcarpeta donde el script `main.py` guarda los vídeos una vez procesados.