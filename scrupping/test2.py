import requests
from bs4 import BeautifulSoup
import json

url = "https://www.voursa.com/Index.cfm?gct=3&gv=13"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    houses = []

    for house_div in soup.find_all('div', id='rptregion'):
        title = house_div.find('div', id='titre').text.strip() if house_div.find('div', id='titre') else "N/A"

        price_div = house_div.find('div', id='prix')
        price = price_div.text.strip() if price_div else "N/A"

        try:
            price = float(price.replace('MRU', '').replace(',', '').strip())
        except ValueError:
            price = float('inf') 

        image_tag = house_div.find('img')
        image_url = image_tag['src'] if image_tag else "N/A"
        image_url = f"https://www.voursa.com{image_url}" if image_url != "N/A" else "N/A"

        link_tag = house_div.find_parent('a')
        link = link_tag['href'] if link_tag else "N/A"
        link = f"https://www.voursa.com{link}" if link != "N/A" else "N/A"

        houses.append({
            'Title': title,
            'Price': price,
            'Image URL': image_url,
            'Link': link
        })

    sorted_houses = sorted(houses, key=lambda x: x['Price'])

    cheapest_houses = sorted_houses[:10]

    json_response = json.dumps(cheapest_houses, ensure_ascii=False, indent=4)

    print(json_response)

else:
    print(f"Failed to retrieve the website. Status code: {response.status_code}")