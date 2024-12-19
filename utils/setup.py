import os
from config.config import Config

def setup_directories():
    """Crear estructura de directorios necesaria"""
    directories = [
        Config.DATA_DIR,
        Config.IMAGES_DIR,
        Config.VIDEOS_DIR,
        Config.REELS_DIR,
        Config.COMMENTS_DIR
    ]
    
    for directory in directories:
        if not directory.exists():
            os.makedirs(directory)
            print(f"Directorio creado: {directory}")
