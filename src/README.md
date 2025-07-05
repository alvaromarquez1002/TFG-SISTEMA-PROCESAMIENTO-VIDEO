# Pipeline de Procesamiento de Datos (Kafka y Spark)

Este directorio contiene toda la lógica, el código y la infraestructura necesarios para el pipeline de procesamiento de vídeo del TFG. El sistema está diseñado para ser modular y está completamente orquestado por Docker.

## Arquitectura del Pipeline

El sistema se basa en tres servicios principales que se despliegan juntos a través de un único fichero `docker-compose.yml`:

1.  **Apache Kafka (Modo KRaft):** Actúa como un broker de mensajería desacoplado. Aunque el script actual no lo utiliza para la ingesta de vídeos, está desplegado como parte de la arquitectura final y está disponible para futuras evoluciones del proyecto hacia un procesamiento basado en eventos.
2.  **Clúster de Apache Spark:** Un clúster simple compuesto por un `spark-master` y un `spark-worker`. Proporciona el entorno de computación distribuida donde se ejecutan los trabajos de análisis de vídeo.
3.  **Procesador de Python (`python-processor`):** Un servicio personalizado que contiene la lógica principal de la aplicación. Su función es encontrar los vídeos de entrada, conectarse al clúster de Spark, ejecutar el trabajo de procesamiento y guardar los resultados.

## Estructura de Ficheros y Directorios

* **`docker-compose.yml`**: Fichero de orquestación principal que define y conecta todos los servicios del pipeline (Kafka, Spark Master, Spark Worker y el procesador de Python).
* **`/dockers/python_processor/`**: Contiene todo lo necesario para construir la imagen del servicio de Python.
    * **`Dockerfile`**: Define la imagen de Python, instalando las dependencias de sistema (como el entorno de Java) y las librerías de Python.
    * **`main.py`**: Es el script principal de la aplicación. Su lógica actual es:
        1.  Buscar el vídeo `.mp4` más antiguo en el directorio de entrada.
        2.  Conectarse al clúster de Spark.
        3.  Aplicar una transformación de prueba (un tinte de color de pantalla dividida) a cada fotograma del vídeo usando OpenCV.
        4.  Guardar el vídeo procesado.
    * **`requirements.txt`**: Lista las dependencias de Python, como `pyspark` y `opencv-python-headless`.
* **`/data/`**: Esta carpeta y su propósito dependen del modo de ejecución.

---

## Guía de Ejecución y Funcionamiento

### El Rol de la Carpeta `/data`

Este proyecto tiene dos flujos de trabajo principales:

1.  **Modo Integrado (Automático con Jitsi):**
    En este modo, el fichero `docker-compose.yml` está configurado para conectar directamente la carpeta donde Jibri guarda las grabaciones con el directorio de entrada de nuestro procesador. La línea clave es:
    `volumes: - /home/alvaro/.jitsi-meet-cfg/jibri/recordings/:/app/data` 
    Esto significa que cuando Jibri graba un vídeo, aparece automáticamente para ser procesado. En este modo, **la carpeta local `src/data/` no se utiliza**.

2.  **Modo de Desarrollo (Pruebas Aisladas):**
    Para probar el pipeline sin depender de Jitsi, puedes:
    * **Comentar** la línea del volumen de Jibri en el `docker-compose.yml`.
    * **Descomentar** (o añadir) la línea: `volumes: - ./data:/app/data`.
    * **Colocar tus propios vídeos de prueba** en la carpeta local `src/data/`.

### Pasos para Ejecutar el Pipeline

1.  **Preparar el Vídeo de Entrada:**
    * Asegúrate de que haya un vídeo `.mp4` disponible en la ubicación de entrada configurada en tu `docker-compose.yml` (ya sea la carpeta de Jibri o la carpeta local `src/data/`).

2.  **Levantar los Servicios:**
    * Desde el directorio `src/`, ejecuta el siguiente comando. Usamos `--build` para asegurarnos de que se utiliza la última versión de tu código en `main.py`.
    ```bash
    docker compose up --build -d
    ```

3.  **Monitorizar y Verificar:**
    * Puedes ver los logs de tu aplicación en tiempo real para seguir el proceso:
    ```bash
    docker compose logs -f python-processor
    ```
    * El log te mostrará la conexión con Spark, el vídeo que está procesando y cuándo finaliza.

4.  **Comprobar el Resultado:**
    * Una vez finalizado el script, el vídeo procesado aparecerá en la subcarpeta `/processed` dentro del directorio de entrada. Por ejemplo, si estás en modo integrado, lo encontrarás en: `/home/alvaro/.jitsi-meet-cfg/jibri/recordings/processed/`.

5.  **Mover los videos ya procesados:**
    * Una vez finalizado el script el video original procesado se mueve a la carpeta `/home/alvaro/.jitsi-meet-cfg/jibri/recordings/archived/` para que la proxima vez que se ejecute el script no pueda volver a analizar ese mismo video cada vez ya que siempre sera el video mas antiguo.

Para una descripcion mas detallada consultar los manuales y demas documentacion
