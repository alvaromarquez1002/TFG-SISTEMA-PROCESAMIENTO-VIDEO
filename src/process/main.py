from pyspark.sql import SparkSession
import cv2 # OpenCV para procesamiento de vídeo
import os # Manejo de archivos y directorios

VIDEO_INPUT_FOLDER = "/app/data" # Carpeta de entrada donde se encuentran los vídeos sin procesar
VIDEO_OUTPUT_FOLDER = "/app/data/processed" # Carpeta de salida donde se guardarán los vídeos procesados
spark = SparkSession.builder \
    .appName("ProcesamientoVideoTFG") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

print("¡Conexión con Spark establecida con éxito!")
print("==========================================")

try:
    # Buscamos el primer archivo .mp4 sin procesar en la carpeta de entrada
    video_file_path = None
    # Buscamos la primera carpeta de grabación que contenga CUALQUIER archivo .mp4
    for root, dirs, files in os.walk(VIDEO_INPUT_FOLDER):
        for file in files:
            if file.endswith('.mp4'):
                # Nos aseguramos de no procesar un vídeo ya procesado
                if "processed" not in root:
                    video_file_path = os.path.join(root, file)
                    break
        # Si ya hemos encontrado un archivo, salimos del bucle
        if video_file_path:
            break

    # Si no se ha encontrado ningún archivo, lanzamos una excepción
    if not video_file_path:
        raise FileNotFoundError("No se ha encontrado ningún archivo .mp4 sin procesar en la carpeta de datos.")

    print(f"Procesando vídeo: {video_file_path}")

    # Abrimos el vídeo con OpenCV
    cap = cv2.VideoCapture(video_file_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Creamos la carpeta de salida si no existe
    os.makedirs(VIDEO_OUTPUT_FOLDER, exist_ok=True)
    # Usamos el nombre original para el archivo de salida + prefijo "procesado_"
    original_filename = os.path.basename(video_file_path)
    output_path = os.path.join(VIDEO_OUTPUT_FOLDER, f"procesado_{original_filename}")

    # Configuramos el escritor de vídeo
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    print("Aplicando transformación simple...")

    # Procesamos el vídeo frame a frame
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Aquí aplicamos una transformación simple: invertir los colores del frame
        processed_frame = cv2.bitwise_not(frame)
        out.write(processed_frame)
        frame_count += 1

    print(f"Procesados {frame_count} frames.")
    print(f"Vídeo procesado guardado en: {output_path}")

    cap.release()
    out.release()

except Exception as e:
    print(f"Ha ocurrido un error: {e}")

# Limpiamos los recursos de Spark
finally:
    spark.stop()
    print("Sesión de Spark detenida.")
    print("==========================================")