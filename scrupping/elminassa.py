from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--window-size=1920,1080")  # Set window size

# Update this path to your ChromeDriver location
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://www.elminassa.com/list"

# Open the URL in the browser
driver.get(url)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(10)

# Get the page source after it's fully loaded
page_source = driver.page_source

# Close the browser
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find all product containers (adjust the class name as per the website structure)
product_containers = soup.find_all('div', class_='swiper-slide')

# List to store all product details
products = []

# Loop through each product container
for container in product_containers:
    try:
        # Extract the image URL (only the first image)
        image_tag = container.find('img', class_='swiper-lazy')
        image_url = image_tag['src'] if image_tag else "No Image"

        # Extract the price
        price_tag = container.find('span', class_='myTopRight2')
        if price_tag:
            # Remove the inner span (e.g., "/ شهر") and get the price text
            for span in price_tag.find_all('span'):
                span.decompose()  # Remove the inner span
            price_text = price_tag.get_text(strip=True)
            # Clean the price string (remove "MRU" and "/شهر", then remove spaces)
            price_text = price_text.replace('MRU', '').replace('/شهر', '').replace(' ', '')
            price = int(price_text) if price_text.isdigit() else "No Price"
        else:
            price = "No Price"

        # Extract the description
        description_tag = container.find('span', class_='myTopLeftt2 arabicFont')
        description = description_tag.get_text(strip=True) if description_tag else "No Description"

        # Extract the item URL (if available)
        item_url_tag = container.find('a', href=True)  # Look for an <a> tag with an href attribute
        if item_url_tag:
            item_url = item_url_tag['href']
            # Construct the full item URL if it's a relative path
            if not item_url.startswith('http'):
                item_url = f"https://www.elminassa.com{item_url}"
        else:
            item_url = "No URL"

        # Store the product details in a dictionary
        product = {
            "image_url": image_url,
            "price": price,
            "description": description,
            "item_url": item_url
        }

        # Add the product to the list
        products.append(product)
    except Exception as e:
        print(f"Error processing a product: {e}")

# Sort products by price (convert price to integer for sorting)
try:
    products.sort(key=lambda x: x['price'] if isinstance(x['price'], int) else float('inf'))
except Exception as e:
    print(f"Error sorting products: {e}")

# Get the 15 cheapest products
cheapest_products = products[:15]

# Print the details of the 15 cheapest products
print("The 15 cheapest products are:")
for index, product in enumerate(cheapest_products, start=1):
    print(f"\nProduct {index}:")
    print(f"Image URL: {product['image_url']}")
    print(f"Price: {product['price']}")
    print(f"Description: {product['description']}")
    print(f"Item URL: {product['item_url']}")