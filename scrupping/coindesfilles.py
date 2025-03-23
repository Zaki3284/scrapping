import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.coindesfilles.net/collections/makeup"
# url = "https://www.coindesfilles.net/collections/nettoyants?page=1"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # List to store product details
    products = []
    
    # Find all product cards
    product_cards = soup.find_all('li', class_='grid__item')
    
    for card in product_cards:
        # Extract product name
        product_name = card.find('h3', class_='card__heading').text.strip()
        
        # Extract product price
        price_container = card.find('div', class_='price__container')
        price = price_container.find('span', class_='price-item--regular').text.strip()
        
        # Convert price to integer for sorting
        price_value = int(''.join(filter(str.isdigit, price)))
        
        # Extract product image URL
        image_tag = card.find('img', class_='motion-reduce')
        image_url = f"https:{image_tag['src']}" if image_tag else "No image available"
        
        # Extract product URL
        product_link_tag = card.find('a', class_='full-unstyled-link')
        product_url = f"https://www.coindesfilles.net{product_link_tag['href']}" if product_link_tag else "No product URL available"
        
        # Append product details to the list
        products.append({
            'name': product_name,
            'price': price_value,
            'image_url': image_url,
            'product_url': product_url
        })
    
    # Sort products by price
    sorted_products = sorted(products, key=lambda x: x['price'])
    
    # Get the 10 cheapest products
    cheapest_products = sorted_products[:10]
    
    # Print the 10 cheapest products with image URLs and product URLs
    for product in cheapest_products:
        print(f"Product: {product['name']}, Price: {product['price']} MRU, Image URL: {product['image_url']}, Product URL: {product['product_url']}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")