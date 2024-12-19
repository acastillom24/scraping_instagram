from utils.setup import setup_directories
from utils.driver import get_driver
from scraper.instagram_login import InstagramLogin
from scraper.content_scraper import ContentScraper
from config.config import Config

def main():
    # Validar credenciales antes de comenzar
    Config.validate_credentials()
    
    # Configurar directorios
    setup_directories()
    
    # Inicializar driver
    driver = get_driver()
    
    try:
        # Login
        login = InstagramLogin(driver)
        if login.login():
            # Iniciar scraping
            scraper = ContentScraper(driver)
            scraper.scrape_profile()
    
    except Exception as e:
        print(f"Error en la ejecución: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
