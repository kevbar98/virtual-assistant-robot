import random

# Lista de mensajes para personas nuevas
NEW_PERSON_MESSAGES = [
    "Hola, bienvenido a la cooperativa Fernando Daquilema.",
    "Hola, es un placer conocerte. Bienvenido.",
    "Hola, gracias por visitarnos."
]

# Lista de mensajes para personas conocidas
WELCOME_BACK_MESSAGES = [
    "Hola, bienvenido de vuelta.",
    "Hola, qué gusto verte nuevamente.",
    "Hola, encantados de verte otra vez."
]

def get_new_person_message():
    """Obtiene un mensaje aleatorio para personas nuevas."""
    return random.choice(NEW_PERSON_MESSAGES)

def get_welcome_back_message():
    """Obtiene un mensaje aleatorio para personas conocidas."""
    return random.choice(WELCOME_BACK_MESSAGES)
