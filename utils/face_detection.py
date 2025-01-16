import cv2
import os
import uuid
import sqlite3
import numpy as np
from datetime import datetime
from deepface import DeepFace
from mtcnn import MTCNN
from utils.audio_output import play_audio
from utils.messages import get_new_person_message, get_welcome_back_message
from utils.logger import log_detection, log_exception
from config import GENERATE_DEBUG_IMAGES, LOG_DETECTIONS_TO_CSV

# Registro temporal para la sesión actual
session_detected_faces = set()

# Inicializar el detector MTCNN
mtcnn_detector = MTCNN()

def init_database():
    """Inicializa la base de datos SQLite."""
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS faces (id TEXT PRIMARY KEY, embedding BLOB, timestamp TEXT)''')
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

def save_new_face(face_id, embedding):
    """Guarda un nuevo rostro en la base de datos."""
    if embedding.shape[0] != 512:
        print(f"Advertencia: el tamaño del embedding no es válido ({embedding.shape[0]}). Registro ignorado.")
        return  # Ignorar el guardado si el tamaño no es válido

    embedding = embedding.astype(np.float32)
    embedding_bytes = embedding.tobytes()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('INSERT INTO faces (id, embedding, timestamp) VALUES (?, ?, ?)', 
              (face_id, embedding_bytes, timestamp))
    conn.commit()
    conn.close()

def detect_and_save_faces(frame):
    """
    Detecta rostros, identifica personas y guarda embeddings únicos.
    Args:
        frame: Frame capturado por la cámara.
    Returns:
        Frame con los rostros detectados marcados.
    """
    global session_detected_faces

    try:
        # Detectar rostros utilizando MTCNN
        faces = mtcnn_detector.detect_faces(frame)

        if not faces:
            # Si no se detectan rostros, no procesar nada
            print("No se detectaron rostros.")
            return frame

        for face in faces:
            x, y, w, h = face['box']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Verde, grosor 2

            # Extraer el rostro de la imagen
            face_image = frame[y:y + h, x:x + w]

            # Verificar que la imagen del rostro no sea vacía
            if face_image.size == 0:
                print("Rostro vacío detectado, saltando.")
                return frame

            # Validar que el rostro no esté completamente negro (esto es cuando la cámara está tapada)
            if np.all(face_image == 0):  # Si todos los valores de la imagen son cero
                print("Imagen de rostro vacía, omitiendo.")
                return frame

            # Generar embeddings usando DeepFace, solo si el rostro es válido
            try:
                # Comprobar si la cara tiene una resolución válida antes de pasarla a DeepFace
                if face_image.shape[0] < 20 or face_image.shape[1] < 20:  # Validar que la cara no sea demasiado pequeña
                    print("Rostro demasiado pequeño para procesar, omitiendo.")
                    return frame

                # Generar embeddings usando DeepFace, solo si el rostro es válido
                representations = DeepFace.represent(img_path=face_image, model_name="ArcFace", enforce_detection=True)
                for rep in representations:
                    embedding = np.array(rep["embedding"])  # Convertir embedding a NumPy array
                    face_id = str(uuid.uuid4())  # ID único para nuevos registros

                    # Comparar con embeddings en la base de datos
                    conn = sqlite3.connect('faces.db')
                    c = conn.cursor()
                    c.execute('SELECT id, embedding FROM faces')
                    known_faces = c.fetchall()

                    is_new_person = True
                    if known_faces:
                        distances = []
                        for row in known_faces:
                            stored_embedding = np.frombuffer(row[1], dtype=np.float32)  # Convertir de bytes a float32
                            if stored_embedding.shape == embedding.shape:  # Verificar tamaños compatibles
                                distances.append((row[0], np.linalg.norm(embedding - stored_embedding)))
                            else:
                                c.execute('DELETE FROM faces WHERE id = ?', (row[0],))  # Eliminar registros corruptos
                                conn.commit()

                        if distances:
                            distances.sort(key=lambda x: x[1])  # Ordenar por distancia
                            min_id, min_distance = distances[0]
                            if min_distance > 0.3 and min_distance < 0.8:  # Ajuste adicional para la distancia
                                is_new_person = False
                                face_id = min_id

                    # Verificar si ya se detectó en esta sesión
                    if face_id not in session_detected_faces:
                        session_detected_faces.add(face_id)
                        if is_new_person:
                            print("Persona nueva detectada.")
                            play_audio(get_new_person_message())
                            save_new_face(face_id, embedding)
                        else:
                            print("Persona conocida detectada.")
                            play_audio(get_welcome_back_message())

                    # Registrar detección en CSV
                    if LOG_DETECTIONS_TO_CSV:
                        log_detection(face_id, (x, y, x + w, y + h))  # Registrar la posición del rostro detectado
                    conn.close()

            except Exception as e:
                print(f"Error durante la generación de embedding: {e}")
                if LOG_DETECTIONS_TO_CSV:
                    log_exception(
                        str(e),
                        {"frame_shape": frame.shape if frame is not None else "No disponible"}
                    )

                if GENERATE_DEBUG_IMAGES:  # Guardar imagen de depuración
                    error_img_path = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(error_img_path, frame)
                    print(f"Imagen guardada para depuración: {error_img_path}")

    except Exception as e:
        print(f"Error durante la detección: {e}")
        if LOG_DETECTIONS_TO_CSV:
            log_exception(str(e), {"frame_shape": frame.shape if frame is not None else "No disponible"})

        if GENERATE_DEBUG_IMAGES:  # Guardar imagen de depuración
            error_img_path = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(error_img_path, frame)
            print(f"Imagen guardada para depuración: {error_img_path}")
    return frame

# Inicializar la base de datos al inicio
init_database()
