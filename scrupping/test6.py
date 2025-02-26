import requests
from bs4 import BeautifulSoup
import json

marque_mapping = {"Toyota": 1, "Mercedes": 2, "Hyundai": 4}
modele_mapping = {
    "Corolla": 24, "avensus": 20, "rav4": 28, "hilux": 25, "tx": 27,
    "accent": 118, "Elantra": 119, "Santa fe": 124, "sonata": 125
}

models_by_brand = {
    "Toyota": {"Corolla": 24, "avensus": 20, "rav4": 28, "hilux": 25, "tx": 27},
    "Hyundai": {"accent": 118, "Elantra": 119, "Santa fe": 124, "sonata": 125},
    "Mercedes": {} 
}

def scrape_cars(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    cars = []

    for car_div in soup.find_all('div', id='rptregion'):
        title = car_div.find('div', id='titre').text.strip() if car_div.find('div', id='titre') else "N/A"
        price_div = car_div.find('div', id='prix')
        price = price_div.text.strip() if price_div else "N/A"

        try:
            price = float(price.replace('MRU', '').replace(',', '').strip())
        except ValueError:
            price = float('inf')

        image_tag = car_div.find('img')
        image_url = f"https://www.voursa.com{image_tag['src']}" if image_tag else "N/A"
        link_tag = car_div.find_parent('a')
        link = f"https://www.voursa.com{link_tag['href']}" if link_tag else "N/A"

        cars.append({
            'Title': title,
            'Price': price,
            'Image_URL': image_url,
            'Link': link
        })

    return sorted(cars, key=lambda x: x['Price'])[:10]

def get_models(brand):
    return models_by_brand.get(brand, {})

def search_cars(brand, model=None):
    av = marque_mapping.get(brand, 0)
    bv = modele_mapping.get(model, 0) if model else 0

    url = f"https://www.voursa.com/Index.cfm?gct=1&sct=11&gv=1&av={av}&bv={bv}&cv=0&dv=0&ev=0&fv=0&genre=0&pp=0&localisation=0&pmin=0&pmax=0"
    print(f"Constructed URL: {url}")
    cars = scrape_cars(url)
    return cars

if __name__ == "__main__":
    brand = input("Enter brand (Toyota, Hyundai, Mercedes): ")
    models = get_models(brand)

    if models:
        print(f"Available models for {brand}: {', '.join(models.keys())}")
        model = input("Enter model (optional): ") if models else None
    else:
        model = None

    results = search_cars(brand, model)
    print(json.dumps(results, indent=4, ensure_ascii=False))
