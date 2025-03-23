from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Path to your WebDriver executable
webdriver_path = "/usr/local/bin/chromedriver"  # Update this path

# Configure Selenium to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--window-size=1920,1080")  # Set window size

# Initialize the WebDriver with headless mode
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the page to scrape
url = "https://beta.mr"

# Open the URL
driver.get(url)

# Wait for the page to load (adjust the sleep time if needed)
time.sleep(10)

# Get the page source after JavaScript has rendered the content
page_source = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find the "Offres d'emploi" section
offres_emploi_section = soup.find('div', class_='card-body bgCard pt-1', style="background-color: #efefff;")

if offres_emploi_section:
    # Find all the job offer cards within the section
    job_offers_cards = offres_emploi_section.find_all('div', class_='card post-card pb-1 mb-1', limit=10)

    # Loop through the first 10 cards and extract the relevant information
    for card in job_offers_cards:
        # Extract the title
        title = card.find('div', class_='post-card-content').text.strip()
        
        # Extract the description
        description = card.find('div', class_='post-card-heading').text.strip()
        
        # Extract the deadline
        deadline = card.find('div', class_='post-card-limit').text.strip()
        
        # Extract the image URL
        image_tag = card.find('img', class_='imgCard')
        image_url = image_tag['src'] if image_tag else "No image found"
        
        # Extract the article URL
        article_link = card.find('a', class_='titleAnn')
        if article_link:
            article_url = article_link['href']
            if not article_url.startswith(('http://', 'https://')):
                article_url = "https://beta.mr" + article_url
        else:
            article_url = "No article URL found"
        
        # Print the extracted information
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Deadline: {deadline}")
        print(f"Image URL: {image_url}")
        print(f"Article URL: {article_url}")
        print("-" * 50)
else:
    print("Offres d'emploi section not found.")