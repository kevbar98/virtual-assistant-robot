import pyttsx3
import threading
from queue import Queue
from config import ENABLE_AUDIO, LOG_DETECTIONS_TO_CSV  # Importar configuraciones desde config.py
from utils.logger import log_audio_event  # Registrar eventos de audio opcionalmente

# Inicializa un único motor de pyttsx3
engine = pyttsx3.init()

# Cola para gestionar solicitudes de audio
audio_queue = Queue()

# Variable global para rastrear el último mensaje reproducido
last_message = None

def audio_worker():
    """Hilo que maneja las solicitudes de reproducción de audio."""
    global last_message
    while True:
        try:
            message = audio_queue.get()  # Obtiene el siguiente mensaje de la cola
            if message is None:
                break  # Finaliza el hilo si recibe `None`

            if message != last_message:  # Evita mensajes repetidos consecutivamente
                if ENABLE_AUDIO:  # Verifica si el audio está habilitado
                    engine.say(message)
                    engine.runAndWait()
                    last_message = message  # Actualiza el último mensaje reproducido
                    if LOG_DETECTIONS_TO_CSV:  # Registrar evento solo si está habilitado
                        log_audio_event("Mensaje reproducido", {"message": message})
                    print(f"Audio reproducido: {message}")
                else:
                    if LOG_DETECTIONS_TO_CSV:  # Registrar evento solo si está habilitado
                        log_audio_event("Audio deshabilitado", {"message": message})
            else:
                if LOG_DETECTIONS_TO_CSV:  # Registrar evento solo si está habilitado
                    log_audio_event("Mensaje repetido ignorado", {"message": message})
                print(f"Mensaje repetido ignorado: {message}")

            audio_queue.task_done()  # Marca la tarea como completada
        except Exception as e:
            if LOG_DETECTIONS_TO_CSV:  # Registrar evento solo si está habilitado
                log_audio_event("Error en reproducción de audio", {"error": str(e)})
            print(f"Error en reproducción de audio: {e}")

# Inicia el hilo de audio
audio_thread = threading.Thread(target=audio_worker, daemon=True)
audio_thread.start()

def play_audio(message):
    """Agrega un mensaje de audio a la cola si el audio está habilitado."""
    if ENABLE_AUDIO:  # Verifica si el audio está habilitado antes de agregarlo a la cola
        audio_queue.put(message)

def stop_audio():
    """Detiene el hilo de audio."""
    audio_queue.put(None)
    audio_thread.join()
