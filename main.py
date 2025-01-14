import cv2
from utils.face_detection import detect_and_save_faces


def real_time_detection():
    """
    Función principal para detección de rostros en tiempo real.
    """
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)

    # Verificar si la cámara está accesible
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    print("Presiona 'q' para salir.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame.")
            break

        # Detectar y procesar rostros
        frame_with_faces = detect_and_save_faces(frame, save_detections=True)

        # Mostrar el video con los rostros detectados
        cv2.imshow("Real-Time Detection", frame_with_faces)

        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Cerrando...")
            break

    # Liberar la cámara y cerrar ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_detection()
