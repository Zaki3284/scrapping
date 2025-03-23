# import requests
# from bs4 import BeautifulSoup
# import json

# url = "https://www.voursa.com/Index.cfm?gct=3&gv=13"
# response = requests.get(url)

# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, 'html.parser')

#     houses = []

#     for house_div in soup.find_all('div', id='rptregion'):
#         title = house_div.find('div', id='titre').text.strip() if house_div.find('div', id='titre') else "N/A"

#         price_div = house_div.find('div', id='prix')
#         price = price_div.text.strip() if price_div else "N/A"

#         try:
#             price = float(price.replace('MRU', '').replace(',', '').strip())
#         except ValueError:
#             price = float('inf') 

#         image_tag = house_div.find('img')
#         image_url = image_tag['src'] if image_tag else "N/A"
#         image_url = f"https://www.voursa.com{image_url}" if image_url != "N/A" else "N/A"

#         link_tag = house_div.find_parent('a')
#         link = link_tag['href'] if link_tag else "N/A"
#         link = f"https://www.voursa.com{link}" if link != "N/A" else "N/A"

#         houses.append({
#             'Title': title,
#             'Price': price,
#             'Image URL': image_url,
#             'Link': link
#         })

#     sorted_houses = sorted(houses, key=lambda x: x['Price'])

#     cheapest_houses = sorted_houses[:10]

#     json_response = json.dumps(cheapest_houses, ensure_ascii=False, indent=4)

#     print(json_response)

# else:
#     print(f"Failed to retrieve the website. Status code: {response.status_code}")

import requests
from bs4 import BeautifulSoup

def scrape_cheapest_cars():
    url = "https://safka.mr/?q=sa1&page=1"
    response = requests.get(url)
    products = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all product rows
        product_rows = soup.find_all('div', class_='views-row')

        for row in product_rows:
            # Extract product name
            product_name_tag = row.find('div', class_='views-field-title')
            product_name = product_name_tag.text.strip() if product_name_tag else "No product name available"

            # Extract product price
            price_tag = row.find('div', class_='views-field-field-prix')
            price = price_tag.text.strip() if price_tag else "No price available"
            # Convert price to a float for sorting
            try:
                price_value = float(price.replace('.', '').replace(',', '.')) if price != "No price available" else float('inf')
            except ValueError:
                price_value = float('inf')  # Handle invalid price formats

            # Extract product image URL
            image_tag = row.find('img')
            image_url = image_tag['src'] if image_tag else "No image available"

            # Extract product URL
            product_url_tag = row.find('a')
            product_url = f"https://www.safka.mr{product_url_tag['href']}" if product_url_tag else "No product URL available"

            # Append product details to the list
            products.append({
                'name': product_name,
                'price': price_value,
                'image_url': image_url,
                'product_url': product_url
            })

        # Sort products by price and get the 10 cheapest
        sorted_products = sorted(products, key=lambda x: x['price'])
        cheapest_products = sorted_products[:10]
    else:
        cheapest_products = []

    return cheapest_products

# Example usage
cheapest_cars = scrape_cheapest_cars()
for car in cheapest_cars:
    print(car)
    
    
