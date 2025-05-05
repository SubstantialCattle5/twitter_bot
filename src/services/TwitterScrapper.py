import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class TwitterScraper:
    def __init__(self,email,password,user_id):
        self.twitter_email = email
        self.twitter_password = password
        self.twitter_user_id = user_id
        self.proxy_routes = [
            "us-ca.proxymesh.com:31280",
        ]
        
    def _proxy_route(self):
        return random.choice(self.proxy_routes)
    
    def _setup(self): 
        
        proxy_route =  "us-ca.proxymesh.com:31280"
        chrome_options = Options()
        chrome_options.add_argument(f'--proxy-server={proxy_route}')
        chrome_options.add_argument('--proxy-bypass-list=*')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        
        return webdriver.Chrome(options=chrome_options)
    
    def _teardown(self,driver):
        driver.quit()
        
    def _login(self, driver):
        """Login to Twitter account."""
        driver.get('https://x.com/i/flow/login')  
        
        try:
            #  Email/username
            email_field = WebDriverWait(driver, 20).until(  
                EC.element_to_be_clickable((By.NAME, "text"))
            )
            email_field.clear()
            email_field.send_keys(self.twitter_email)
            
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
            )
            next_button.click()
            
            # Step 2: Handle unusual activity
            time.sleep(3)  
            if "unusual login activity" in driver.page_source.lower():
                username_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "text"))
                )
                username_field.clear()
                username_field.send_keys(self.twitter_user_id)
                
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                )
                next_button.click()
            
            # Step 3: Password
            password_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_field.clear()
            password_field.send_keys(self.twitter_password)
            
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
            )
            login_button.click()
            
            # Wait for home page to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Home timeline']"))
            )
            
            time.sleep(5)  # Allow page to fully load

        except Exception as e:
            print(f"Login failed: {str(e)}")
            driver.save_screenshot(f"error_login_{int(time.time())}.png")
            raise 

    def get_latest_trends(self):
        """Get trending topics on Twitter."""
        driver = None

        try:
            driver = self._setup()
            self._login(driver)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            trends = []
            trend_elements = soup.find_all('span', {'class': 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3'})
            
            for trend in trend_elements:
                trend_text = trend.get_text(strip=True)

                # Check if the trend starts with a hashtag
                if trend_text.startswith('#'):
                    trends.append(trend_text)

            return trends

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            if driver:
                driver.save_screenshot(f"error_trends_{int(time.time())}.png")
            return None

        finally:
            if driver:
                self._teardown(driver)


