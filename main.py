import cv2
from utils.face_detection import detect_and_save_faces
import threading
import time

# Variable global para controlar la detección de rostros
detection_blocked = False

def detection_listener():
    """Escucha los cambios de la variable `detection_blocked`."""
    global detection_blocked

    while True:
        if not detection_blocked:
            print("La detección de rostros está habilitada.")
            # Aquí reactivamos la detección si es necesario
            break  # Sale del ciclo una vez que la detección se reanuda

        time.sleep(1)  # Espera 1 segundo antes de revisar el estado nuevamente

def real_time_detection():
    """Función principal para detección de rostros en tiempo real usando DeepFace."""
    global detection_blocked

    # Iniciar el hilo que escucha el cambio de estado
    listener_thread = threading.Thread(target=detection_listener, daemon=True)
    listener_thread.start()

    # Inicializamos la cámara y la detección
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara. Verifica la conexión o si está siendo usada por otra aplicación.")
        return

    print("Presiona 'q' para salir.")
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error al capturar el frame.")
                break

            # Si la detección está habilitada, realizar la detección
            if not detection_blocked:
                # Detectar y procesar rostros
                frame_with_faces = detect_and_save_faces(frame)

            cv2.imshow("Real-Time Detection", frame_with_faces)

            # Salir si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Cerrando...")
                break

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_detection()
