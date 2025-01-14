import cv2
import os
import uuid
import torch
from datetime import datetime
from facenet_pytorch import MTCNN, InceptionResnetV1
from config import DATA_PATHS
from utils.audio_output import play_audio
from utils.logger import log_detection
from utils import messages  # Esto indica que 'messages' está dentro del paquete 'utils'

# Inicializa MTCNN y el modelo de reconocimiento facial
mtcnn = MTCNN(keep_all=True, device=torch.device("cpu"))  # Cambia a "cuda" si usas GPU
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Cargar las huellas faciales de personas conocidas
known_face_encodings = []  # Lista para almacenar embeddings faciales
known_face_directories = {}  # Diccionario para almacenar UUID de personas y sus directorios

def load_known_faces():
    """
    Carga las huellas faciales y las carpetas de personas conocidas desde data/faces/.
    """
    global known_face_encodings, known_face_directories
    for folder_name in os.listdir(DATA_PATHS["faces"]):
        folder_path = os.path.join(DATA_PATHS["faces"], folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if file_name.endswith(".jpg"):
                    # Cargar la imagen y calcular su embedding facial
                    img = cv2.imread(file_path)
                    img_cropped = mtcnn(img)  # Detectar y recortar rostro
                    if img_cropped is not None:
                        if len(img_cropped.shape) == 3:
                            img_cropped = img_cropped.unsqueeze(0)  # Asegura que sea un tensor 4D
                        embedding = resnet(img_cropped).detach().numpy()
                        known_face_encodings.append(embedding[0])
                        known_face_directories[folder_name] = folder_path

def detect_and_save_faces(frame, save_detections=True):
    """
    Detecta rostros en un frame, reconoce personas y organiza las fotos en carpetas únicas.
    Args:
        frame: Frame capturado por la cámara.
        save_detections: Booleano, guarda rostros detectados si es True.
    Returns:
        Frame con los rostros detectados encerrados en rectángulos.
    """
    global known_face_encodings, known_face_directories

    # Detectar rostros usando MTCNN
    boxes, _ = mtcnn.detect(frame)

    if boxes is not None:
        for i, box in enumerate(boxes):
            # Coordenadas del rostro
            x1, y1, x2, y2 = [int(coord) for coord in box]

            # Recortar el rostro detectado
            face = frame[y1:y2, x1:x2]

            # Verificar si el rostro está vacío
            if face.size == 0:
                continue

            # Obtener el embedding del rostro detectado
            face_cropped = mtcnn(face)
            if face_cropped is not None:
                # Ajusta las dimensiones si es necesario
                if len(face_cropped.shape) == 3:
                    face_cropped = face_cropped.unsqueeze(0)
                elif len(face_cropped.shape) > 4:
                    face_cropped = face_cropped.squeeze(0)

                # Genera el embedding
                face_embedding = resnet(face_cropped).detach().numpy()[0]

                # Comparar con embeddings conocidos
                if len(known_face_encodings) > 0:
                    distances = [torch.dist(torch.tensor(face_embedding), torch.tensor(known_encoding))
                                 for known_encoding in known_face_encodings]
                    min_distance = min(distances)
                    if min_distance < 0.6:  # Umbral para reconocimiento facial
                        matched_index = distances.index(min_distance)

                        # Validar que matched_index esté dentro de los límites
                        keys = list(known_face_directories.keys())
                        if 0 <= matched_index < len(keys):
                            person_id = keys[matched_index]
                            person_folder = known_face_directories[person_id]
                            play_audio(messages.WELCOME_BACK_MESSAGE)
                        else:
                            print(f"Error: matched_index ({matched_index}) fuera de rango.")
                            continue
                    else:
                        # Persona nueva
                        person_id = str(uuid.uuid4())
                        person_folder = os.path.join(DATA_PATHS["faces"], person_id)
                        os.makedirs(person_folder, exist_ok=True)
                        play_audio(messages.NEW_PERSON_MESSAGE)

                        # Agregar al registro de rostros conocidos
                        known_face_encodings.append(face_embedding)
                        known_face_directories[person_id] = person_folder
                else:
                    # No hay rostros conocidos; registrar el primero
                    person_id = str(uuid.uuid4())
                    person_folder = os.path.join(DATA_PATHS["faces"], person_id)
                    os.makedirs(person_folder, exist_ok=True)
                    play_audio(messages.NEW_PERSON_MESSAGE)

                    known_face_encodings.append(face_embedding)
                    known_face_directories[person_id] = person_folder

                # Guardar la foto en la carpeta correspondiente
                if save_detections:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    face_path = os.path.join(person_folder, f"{timestamp}.jpg")
                    cv2.imwrite(face_path, face)

                # Dibujar un rectángulo alrededor del rostro
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    return frame

# Cargar rostros conocidos al inicio
load_known_faces()
