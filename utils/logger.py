from config import LOG_DETECTIONS_TO_CSV
import csv
import os
import json
from datetime import datetime


def ensure_log_directory(log_file):
    """
    Crea la carpeta para el archivo de log si no existe.
    Args:
        log_file (str): Ruta del archivo de log.
    """
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def log_exception(exception_message, frame_info=None):
    """
    Registra una excepción en el archivo CSV si está habilitado.
    Args:
        exception_message (str): Mensaje de la excepción.
        frame_info (dict): Información adicional sobre el frame procesado (opcional).
    """
    if not LOG_DETECTIONS_TO_CSV:
        return  # Salir si el registro está deshabilitado

    log_file = "logs/exceptions.csv"
    try:
        ensure_log_directory(log_file)

        with open(log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            frame_info_str = json.dumps(frame_info) if frame_info else "No disponible"
            writer.writerow([timestamp, exception_message, frame_info_str])

    except Exception as e:
        print(f"Error al registrar excepción: {e}")


def log_detection(face_id, position):
    """
    Registra una detección en el archivo CSV si está habilitado.
    Args:
        face_id (str): Identificador único del rostro detectado.
        position (tuple): Coordenadas del rostro (x, y, w, h).
    """
    if not LOG_DETECTIONS_TO_CSV:
        return  # Salir si el registro está deshabilitado

    log_file = "logs/detections.csv"
    try:
        ensure_log_directory(log_file)

        with open(log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, face_id, position])

    except Exception as e:
        print(f"Error al registrar detección: {e}")


def log_audio_event(event_message, details=None):
    """
    Registra un evento relacionado con el audio en el archivo CSV si está habilitado.
    Args:
        event_message (str): Descripción del evento de audio.
        details (dict): Información adicional sobre el evento (opcional).
    """
    if not LOG_DETECTIONS_TO_CSV:
        return  # Salir si el registro está deshabilitado

    log_file = "logs/audio_events.csv"
    try:
        ensure_log_directory(log_file)

        with open(log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            details_str = json.dumps(details) if details else "No disponible"
            writer.writerow([timestamp, event_message, details_str])

    except Exception as e:
        print(f"Error al registrar evento de audio: {e}")
