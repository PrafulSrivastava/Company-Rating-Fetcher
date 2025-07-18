import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service

# TODO: Implement `gather_all_ratings(company: str, location: str) -> list[dict]`
# and classes:
#   - TrustpilotScraper.get_rating(company) → {source, rating, error?}
#   - GlassdoorScraper.get_rating(company, location) → {source, rating, error?}
# Include stub classes for Comparably and LevelsFyi.

class TrustpilotScraper:
    @staticmethod
    def get_rating(company: str) -> dict:
        url = f"https://www.trustpilot.com/review/{company}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            h2 = soup.find('h2')
            rating = None
            if h2:
                rating = h2.get_text(strip=True)
            return {"source": "Trustpilot", "rating": rating}
        except Exception as e:
            return {"source": "Trustpilot", "rating": None, "error": str(e)}

class GlassdoorScraper:
    def __init__(self, driver_path: str = None):
        self.driver_path = driver_path or os.environ.get('CHROMEDRIVER_PATH')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        if self.driver_path:
            service = Service(executable_path=self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)

    def get_rating(self, company: str, location: str) -> dict:
        url = 'https://www.glassdoor.com/Reviews/index.htm'
        try:
            self.driver.get(url)
            time.sleep(2)
            search_box = self.driver.find_element(By.ID, 'KeywordSearch')
            location_box = self.driver.find_element(By.ID, 'LocationSearch')
            search_box.clear()
            search_box.send_keys(company)
            location_box.clear()
            location_box.send_keys(location)
            location_box.send_keys(Keys.RETURN)
            time.sleep(3)
            rating_elem = self.driver.find_elements(By.CSS_SELECTOR, '.ehrRating')
            rating = rating_elem[0].text if rating_elem else None
            return {"source": "Glassdoor", "rating": rating}
        except Exception as e:
            return {"source": "Glassdoor", "rating": None, "error": str(e)}
        finally:
            self.driver.quit()

def gather_all_ratings(company: str, location: str) -> list[dict]:
    results = []
    # Trustpilot
    trustpilot_result = TrustpilotScraper.get_rating(company)
    results.append(trustpilot_result)
    # Glassdoor
    glassdoor_scraper = GlassdoorScraper()
    glassdoor_result = glassdoor_scraper.get_rating(company, location)
    results.append(glassdoor_result)
    # GlassdoorScraper closes driver in get_rating
    return results
