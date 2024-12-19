import json
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config

class ContentScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def scrape_profile(self):
        """Extraer contenido del perfil objetivo"""
        try:
            # Navegar al perfil
            self.driver.get(f"{Config.BASE_URL}/{Config.TARGET_PROFILE}")
            time.sleep(3)
            
            # Obtener publicaciones
            posts = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "article a")
                )
            )
            
            for post in posts:
                # Abrir publicación
                post.click()
                time.sleep(2)
                
                # Determinar tipo de contenido
                if self._is_image():
                    self._download_image()
                elif self._is_video():
                    self._download_video()
                elif self._is_reel():
                    self._download_reel()
                
                # Extraer comentarios
                self._extract_comments()
                
                # Cerrar publicación
                close_button = self.driver.find_element(
                    By.CSS_SELECTOR, "svg[aria-label='Cerrar']"
                )
                close_button.click()
                time.sleep(1)
        
        except Exception as e:
            print(f"Error durante el scraping: {str(e)}")
    
    def _is_image(self):
        """Verificar si la publicación es una imagen"""
        try:
            self.driver.find_element(By.CSS_SELECTOR, "img[style*='object-fit: cover']")
            return True
        except:
            return False
    
    def _is_video(self):
        """Verificar si la publicación es un video"""
        try:
            self.driver.find_element(By.TAG_NAME, "video")
            return True
        except:
            return False
    
    def _is_reel(self):
        """Verificar si la publicación es un reel"""
        try:
            self.driver.find_element(By.CSS_SELECTOR, "[role='button'][tabindex='0']")
            return True
        except:
            return False
    
    def _download_image(self):
        """Descargar imagen"""
        try:
            img = self.driver.find_element(
                By.CSS_SELECTOR, "img[style*='object-fit: cover']"
            )
            img_url = img.get_attribute("src")
            
            # Generar nombre único
            filename = f"{int(time.time())}.jpg"
            filepath = Config.IMAGES_DIR / filename
            
            # Descargar imagen
            response = requests.get(img_url)
            with open(filepath, "wb") as f:
                f.write(response.content)
                
            print(f"Imagen guardada: {filename}")
        
        except Exception as e:
            print(f"Error al descargar imagen: {str(e)}")
    
    def _download_video(self):
        """Descargar video"""
        try:
            video = self.driver.find_element(By.TAG_NAME, "video")
            video_url = video.get_attribute("src")
            
            filename = f"{int(time.time())}.mp4"
            filepath = Config.VIDEOS_DIR / filename
            
            response = requests.get(video_url)
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            print(f"Video guardado: {filename}")
        
        except Exception as e:
            print(f"Error al descargar video: {str(e)}")
    
    def _download_reel(self):
        """Descargar reel"""
        try:
            video = self.driver.find_element(By.TAG_NAME, "video")
            video_url = video.get_attribute("src")
            
            filename = f"{int(time.time())}.mp4"
            filepath = Config.REELS_DIR / filename
            
            response = requests.get(video_url)
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            print(f"Reel guardado: {filename}")
        
        except Exception as e:
            print(f"Error al descargar reel: {str(e)}")
    
    def _extract_comments(self):
        """Extraer comentarios de la publicación"""
        try:
            # Cargar más comentarios si están disponibles
            while True:
                try:
                    load_more = self.driver.find_element(
                        By.XPATH, "//button[contains(text(), 'Cargar más comentarios')]"
                    )
                    load_more.click()
                    time.sleep(1)
                except:
                    break
            
            # Extraer comentarios
            comments = self.driver.find_elements(
                By.CSS_SELECTOR, "ul ul div[role='button']"
            )
            
            comments_data = []
            for comment in comments:
                try:
                    username = comment.find_element(
                        By.CSS_SELECTOR, "a"
                    ).text
                    text = comment.find_element(
                        By.CSS_SELECTOR, "span"
                    ).text
                    
                    comments_data.append({
                        "username": username,
                        "text": text,
                        "timestamp": int(time.time())
                    })
                except:
                    continue
            
            # Guardar comentarios
            if comments_data:
                filename = f"comments_{int(time.time())}.json"
                filepath = Config.COMMENTS_DIR / filename
                
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(comments_data, f, ensure_ascii=False, indent=2)
                
                print(f"Comentarios guardados: {filename}")
        
        except Exception as e:
            print(f"Error al extraer comentarios: {str(e)}")
