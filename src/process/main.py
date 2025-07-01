from pyspark.sql import SparkSession

print("==========================================")
print("Iniciando script de procesamiento de vídeo...")
print("==========================================")

try:
    # --- 1. Creación de la Sesión de Spark ---
    # Nos conectamos al Spark Master que está corriendo en Docker
    spark = SparkSession.builder \
        .appName("ProcesamientoVideoTFG") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    print("¡Conexión con Spark establecida con éxito!")
    print(f"Versión de Spark: {spark.version}")
    print("==========================================")

    # --- 2. Operación de Prueba ---
    # Probar que el clúster funciona
    data = [("Prueba de Conexión", 1)]
    df = spark.createDataFrame(data, ["mensaje", "id"])

    print("DataFrame de prueba creado. Mostrando contenido:")
    df.show()

except Exception as e:
    print(f"Ha ocurrido un error: {e}")

finally:
    # --- 3. Detener la Sesión ---
    # Es importante detener la sesión para liberar los recursos
    if 'spark' in locals():
        spark.stop()
        print("Sesión de Spark detenida.")

    print("Proceso de prueba finalizado.")
    print("==========================================")