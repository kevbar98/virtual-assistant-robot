import csv
import os
from datetime import datetime

def log_detection(face_id, position):
    """
    Registra una detección en un archivo CSV.

    Args:
        face_id (str): Identificador único del rostro detectado.
        position (tuple): Coordenadas (x, y, w, h) del rostro.
    """
    # Ruta del archivo de registro
    log_file = "logs/detections.csv"

    # Crear la carpeta logs si no existe
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Escribir la detección en el archivo CSV
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Obtener la marca de tiempo actual
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Escribir el identificador del rostro, las coordenadas y la marca de tiempo
        writer.writerow([face_id, position, timestamp])
