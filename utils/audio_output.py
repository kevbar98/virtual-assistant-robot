import pyttsx3
import threading
from queue import Queue

# Inicializa un único motor de pyttsx3
engine = pyttsx3.init()

# Cola para gestionar solicitudes de audio
audio_queue = Queue()

def audio_worker():
    """Hilo que maneja las solicitudes de reproducción de audio."""
    while True:
        message = audio_queue.get()  # Obtiene el siguiente mensaje de la cola
        if message is None:
            break  # Finaliza el hilo si recibe `None`
        engine.say(message)
        engine.runAndWait()
        audio_queue.task_done()  # Marca la tarea como completada

# Inicia el hilo de audio
audio_thread = threading.Thread(target=audio_worker, daemon=True)
audio_thread.start()

def play_audio(message):
    """Agrega un mensaje de audio a la cola."""
    audio_queue.put(message)

def stop_audio():
    """Detiene el hilo de audio."""
    audio_queue.put(None)
    audio_thread.join()
