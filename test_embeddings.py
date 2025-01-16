from deepface import DeepFace
import numpy as np

# Imagen de prueba
test_image = "C:/git/virtual-assistant/data/test/rostro_prueba.jpg"



# Generar embedding
representations = DeepFace.represent(img_path=test_image, model_name="ArcFace", enforce_detection=False)

for rep in representations:
    embedding = np.array(rep["embedding"])
    print(f"Tamaño del embedding generado: {embedding.shape}")
