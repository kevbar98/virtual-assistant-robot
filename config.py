# config.py

# Configuración de datos
DATA_PATHS = {
    "raw": "data/raw/",
    "train": "data/train/",
    "test": "data/test/",
    "val": "data/val/",
    "faces": "data/faces/"
}

# Configuración de detección
SAVE_DETECTIONS = True  # Habilita o deshabilita guardar rostros detectados

# Configuración para habilitar o deshabilitar el audio
ENABLE_AUDIO = True  # Cambiar a False para deshabilitar el audio

# Configuración para habilitar o deshabilitar los logs
LOG_DETECTIONS_TO_CSV = True

# Configuración para generar imágenes de depuración
GENERATE_DEBUG_IMAGES = True  # Cambiar a False para deshabilitar la depuración con imágenes

