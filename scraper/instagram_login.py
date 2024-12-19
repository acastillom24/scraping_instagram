from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config

class InstagramLogin:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def login(self):
        """Realizar login en Instagram"""
        try:
            self.driver.get(Config.BASE_URL)
            
            # Esperar y completar campos de login
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = self.driver.find_element(By.NAME, "password")
            
            username_input.send_keys(Config.USERNAME)
            password_input.send_keys(Config.PASSWORD)
            
            # Click en botón de login
            login_button = self.driver.find_element(
                By.XPATH, "//button[@type='submit']"
            )
            login_button.click()
            
            # Esperar a que se complete el login
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Inicio']"))
            )
            
            return True
        except Exception as e:
            print(f"Error durante el login: {str(e)}")
            return False
