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
    ## Bloque para buscar y ordenar todos los vídeos por fecha
    candidate_videos = []
    # 1. Recorremos todo el directorio y encontramos TODOS los vídeos candidatos
    for root, dirs, files in os.walk(VIDEO_INPUT_FOLDER):
        # Excluimos la carpeta 'processed' del recorrido
        if "processed" in dirs:
            dirs.remove("processed")
            
        for file in files:
            if file.endswith('.mp4'):
                full_path = os.path.join(root, file)
                # Obtenemos la fecha de modificación del archivo
                mod_time = os.path.getmtime(full_path)
                candidate_videos.append((full_path, mod_time))

    video_file_path = None
    # 2. Si hemos encontrado vídeos, los ordenamos por fecha y elegimos el más antiguo
    if candidate_videos:
        # Ordenamos la lista de vídeos por su fecha de modificación
        candidate_videos.sort(key=lambda x: x[1])
        # El vídeo a procesar es el primero de la lista (el más antiguo)
        video_file_path = candidate_videos[0][0]

    if not video_file_path:
        raise FileNotFoundError("No se ha encontrado ningún archivo .mp4 sin procesar en la carpeta de grabaciones.")

    print(f"Procesando el vídeo más antiguo: {video_file_path}")

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

        # --- INICIO DE LA TRANSFORMACIÓN DE PANTALLA DIVIDIDA ---
        
        # Hacemos una copia del frame para no modificar el original directamente en el bucle
        processed_frame = frame.copy()
        
        # Calculamos el punto medio de la pantalla
        mid_point = frame_width // 2
        
        # Creamos una capa de color azul para la mitad izquierda
        overlay_left = processed_frame.copy()
        cv2.rectangle(overlay_left, (0, 0), (mid_point, frame_height), (255, 0, 0), -1) # BGR: Azul

        # Creamos una capa de color rojo para la mitad derecha
        overlay_right = processed_frame.copy()
        cv2.rectangle(overlay_right, (mid_point, 0), (frame_width, frame_height), (0, 0, 255), -1) # BGR: Rojo
        
        # Mezclamos la mitad izquierda del frame con la capa azul semi-transparente
        processed_frame[:, :mid_point] = cv2.addWeighted(frame[:, :mid_point], 0.7, overlay_left[:, :mid_point], 0.3, 0)
        
        # Mezclamos la mitad derecha del frame con la capa roja semi-transparente
        processed_frame[:, mid_point:] = cv2.addWeighted(frame[:, mid_point:], 0.7, overlay_right[:, mid_point:], 0.3, 0)
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