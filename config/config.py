from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

class Config:
    # Directorios base
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    # Subdirectorios para diferentes tipos de contenido
    IMAGES_DIR = DATA_DIR / "images"
    VIDEOS_DIR = DATA_DIR / "videos"
    REELS_DIR = DATA_DIR / "reels"
    COMMENTS_DIR = DATA_DIR / "comments"
    
    # Credenciales de Instagram desde variables de entorno
    USERNAME = os.getenv('INSTAGRAM_USERNAME')
    PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
    
    # Validación de credenciales
    @classmethod
    def validate_credentials(cls):
        if not cls.USERNAME or not cls.PASSWORD:
            raise ValueError(
                "Las credenciales de Instagram no están configuradas. "
                "Asegúrate de crear un archivo .env con INSTAGRAM_USERNAME y INSTAGRAM_PASSWORD"
            )
    
    # URLs
    BASE_URL = "https://www.instagram.com"
    TARGET_PROFILE = "entel"
    
    # Configuración de esperas
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
