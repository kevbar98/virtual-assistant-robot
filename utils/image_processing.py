import cv2
import torch
from torchvision import transforms

def load_image(image_path, image_size):
    """Carga y procesa una imagen desde una ruta."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize(image_size),
        transforms.Normalize([0.5], [0.5])
    ])
    return transform(image)
