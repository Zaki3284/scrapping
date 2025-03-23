from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of the page to scrape
url = "https://mr.opensooq.com/ar/سيارات-ومركبات/سيارات-للبيع"

# Open the page
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time as needed

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# List to store product details
products = []

# Find all product cards
product_cards = soup.find_all('a', class_='postListItemData')

for card in product_cards:
    # Extract product title
    title_tag = card.find('h2', class_='breakWord')
    title = title_tag.text.strip() if title_tag else "No title available"
    
    # Extract product price
    price_tag = card.find('div', class_='priceColor')
    price = price_tag.text.strip() if price_tag else "No price available"
    
    # Extract product location
    location_tag = card.find('div', class_='darkGrayColor')
    location = location_tag.text.strip() if location_tag else "No location available"
    
    # Extract product description
    description_tag = card.find('p')
    description = description_tag.text.strip() if description_tag else "No description available"
    
    # Extract product image URLs
    image_tags = card.find_all('img', class_='width-100 height-100')
    image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]
    
    # Extract product URL
    product_url = card['href'] if 'href' in card.attrs else "No product URL available"
    product_url = f"https://mr.opensooq.com{product_url}"  # Convert to absolute URL
    
    # Append product details to the list
    products.append({
        'title': title,
        'price': price,
        'location': location,
        'description': description,
        'image_urls': image_urls,
        'product_url': product_url
    })

# Print the scraped product details
for product in products:
    print(f"Title: {product['title']}")
    print(f"Price: {product['price']}")
    print(f"Location: {product['location']}")
    print(f"Description: {product['description']}")
    print(f"Image URLs: {product['image_urls']}")
    print(f"Product URL: {product['product_url']}")
    print("-" * 50)

# Close the browser
driver.quit()