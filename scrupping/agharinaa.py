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
service = Service("/usr/local/bin/chromedriver")  # Replace with the path to your ChromeDriver

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the URL
    url = "https://www.agharinaa.com/residentiels-louer"
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)  # Adjust the sleep time as needed
    
    # Get the page source
    page_source = driver.page_source
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # List to store property details
    properties = []
    
    # Find all property listings
    listings = soup.find_all('div', class_='cursor-pointer')
    
    for listing in listings:
        # Extract the image URL
        image = listing.find('img', class_='w-full h-48 object-cover')
        image_url = image['src'] if image else 'Image not available'
        
        # Extract the title
        title = listing.find('h3', class_='text-xl font-bold text-gray-900 line-clamp-1 overflow-hidden')
        title_text = title.text.strip() if title else 'Title not available'
        
        # Extract the location
        location = listing.find('p', class_='text-sm text-gray-600')
        location_text = location.text.strip() if location else 'Location not available'
        
        # Extract the price
        price = listing.find('span', class_='text-lg font-bold text-gray-800')
        price_text = price.text.strip() if price else 'Price not available'
        
        # Extract the number of rooms, bathrooms, garages, and pool availability
        features = listing.find_all('div', class_='flex items-center gap-x-2')
        rooms = features[0].text.strip() if len(features) > 0 else 'Rooms not available'
        bathrooms = features[1].text.strip() if len(features) > 1 else 'Bathrooms not available'
        garages = features[2].text.strip() if len(features) > 2 else 'Garages not available'
        pool = features[3].text.strip() if len(features) > 3 else 'Pool not available'
        
        # Append property details to the list
        properties.append({
            'title': title_text,
            'location': location_text,
            'price': price_text,
            'rooms': rooms,
            'bathrooms': bathrooms,
            'garages': garages,
            'pool': pool,
            'image_url': image_url
        })
    
    # Print the scraped property details
    for property in properties:
        print(f"Title: {property['title']}")
        print(f"Location: {property['location']}")
        print(f"Price: {property['price']}")
        print(f"Rooms: {property['rooms']}")
        print(f"Bathrooms: {property['bathrooms']}")
        print(f"Garages: {property['garages']}")
        print(f"Pool: {property['pool']}")
        print(f"Image URL: {property['image_url']}")
        print("-" * 50)
finally:
    # Close the WebDriver
    driver.quit()










# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from bs4 import BeautifulSoup

# # Set up Selenium WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # Open the URL
# url = "https://www.agharinaa.com/residentiels-louer"
# driver.get(url)

# # Wait for the page to load
# time.sleep(5)

# # Get the page source
# html = driver.page_source

# # Parse the HTML with BeautifulSoup
# soup = BeautifulSoup(html, 'html.parser')

# # Find all the property listings
# listings = soup.find_all('div', class_='cursor-pointer')
# print(f"Number of listings found: {len(listings)}")

# # Iterate over each listing and extract the required information
# for listing in listings:
#     # Extract the image URL
#     image = listing.find('img', class_='w-full h-48 object-cover')
#     image_url = image['src'] if image else 'Image not available'
    
#     # Extract the title
#     title = listing.find('h3', class_='text-xl font-bold text-gray-900 line-clamp-1 overflow-hidden')
#     title_text = title.text.strip() if title else 'Title not available'
    
#     # Extract the location
#     location = listing.find('p', class_='text-sm text-gray-600')
#     location_text = location.text.strip() if location else 'Location not available'
    
#     # Extract the price
#     price = listing.find('span', class_='text-lg font-bold text-gray-800')
#     price_text = price.text.strip() if price else 'Price not available'
    
#     # Extract the number of rooms, bathrooms, garages, and pool availability
#     features = listing.find_all('div', class_='flex items-center gap-x-2')
#     rooms = features[0].text.strip() if len(features) > 0 else 'Rooms not available'
#     bathrooms = features[1].text.strip() if len(features) > 1 else 'Bathrooms not available'
#     garages = features[2].text.strip() if len(features) > 2 else 'Garages not available'
#     pool = features[3].text.strip() if len(features) > 3 else 'Pool not available'
    
#     # Print the extracted information
#     print(f"Title: {title_text}")
#     print(f"Location: {location_text}")
#     print(f"Price: {price_text}")
#     print(f"Rooms: {rooms}")
#     print(f"Bathrooms: {bathrooms}")
#     print(f"Garages: {garages}")
#     print(f"Pool: {pool}")
#     print(f"Image URL: {image_url}")
#     print("-" * 40)

# # Close the browser
# driver.quit()