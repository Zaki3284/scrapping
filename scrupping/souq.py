from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection

# Path to your ChromeDriver
service = Service("/usr/local/bin/chromedriver") # Replace with the path to your ChromeDriver

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the URL
    url = "https://souq.mr/product-category/الرجل/"
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)  # Adjust the sleep time as needed
    
    # Get the page source
    page_source = driver.page_source
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # List to store product details
    products = []
    
    # Find all product cards
    product_cards = soup.find_all('div', class_='product-wrapper')
    
    for card in product_cards:
        # Extract product name
        product_name_tag = card.find('h3', class_='wd-entities-title')
        product_name = product_name_tag.text.strip() if product_name_tag else "No product name available"
        
        # Extract product price
        price_tag = card.find('span', class_='price')
        if price_tag:
            original_price = price_tag.find('del')
            discounted_price = price_tag.find('ins')
            price = discounted_price.text.strip() if discounted_price else original_price.text.strip() if original_price else "No price available"
        else:
            price = "No price available"
        
        # Extract product image URL
        image_tag = card.find('img', class_='attachment-woocommerce_thumbnail')
        image_url = image_tag['src'] if image_tag else "No image available"
        
        # Extract product URL
        product_url_tag = card.find('a', class_='product-image-link')
        product_url = product_url_tag['href'] if product_url_tag else "No product URL available"
        
        # Append product details to the list
        products.append({
            'name': product_name,
            'price': price,
            'image_url': image_url,
            'product_url': product_url
        })
    
    # Print the scraped product details
    for product in products:
        print(f"Product: {product['name']}")
        print(f"Price: {product['price']}")
        print(f"Image URL: {product['image_url']}")
        print(f"Product URL: {product['product_url']}")
        print("-" * 50)
finally:
    # Close the WebDriver
    driver.quit()
    
# base_url = "https://souq.mr/product-category/الرجل/page/{}/"
# for page in range(1, 5):  # Scrape the first 4 pages
#     url = base_url.format(page)
#     response = session.get(url, headers=headers)