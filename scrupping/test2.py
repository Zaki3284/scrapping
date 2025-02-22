from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.voursa.com/index.cfm?gct=1&sct=11&gv=13'
options = Options()
options.headless = True  

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)

driver.implicitly_wait(10)

listings = driver.find_elements(By.CSS_SELECTOR, 'div.listing a')

for listing in listings:
    title = listing.find_element(By.CLASS_NAME, 'titre').text if listing.find_element(By.CLASS_NAME, 'titre') else 'N/A'
    price = listing.find_element(By.CLASS_NAME, 'prix').text if listing.find_element(By.CLASS_NAME, 'prix') else 'N/A'
    image = listing.find_element(By.CLASS_NAME, 'photo').find_element(By.TAG_NAME, 'img').get_attribute('src') if listing.find_element(By.CLASS_NAME, 'photo') else 'No image'
    link = listing.get_attribute('href') if listing.get_attribute('href') else 'No link'

    print(f"Title: {title} | Price: {price} | Image: {image} | Link: {link}")

driver.quit()
