# config.py

# Configuración de datos
DATA_PATHS = {
    "raw": "data/raw/",
    "train": "data/train/",
    "test": "data/test/",
    "val": "data/val/",
    "faces": "data/faces/"
}

# Configuración del modelo
MODEL_PATH = "models/facetracker.pth"

# Configuración de imágenes
IMAGE_SIZE = (120, 120)

# Configuración de entrenamiento
BATCH_SIZE = 8
EPOCHS = 10
LEARNING_RATE = 0.001

# Configuración de detección
SAVE_DETECTIONS = True  # Habilita o deshabilita guardar rostros detectados

# Mensaje de detección
DETECTION_MESSAGE = "Se detectó un rostro. Bienvenido al sistema."
