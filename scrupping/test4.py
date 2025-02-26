import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.voursa.com/index.cfm"

params = {
    "gct": 1,  # Catégorie (Voitures)
    "sct": 11,  # Sous-catégorie
    "gv": 1,   # Marque (Brand)
    "av": 6,   # Modèle "Corolla" (selon le mapping)
    "bv": 0,   # Boîte de vitesse (toutes)
    "cv": 0,   # Année de modèle (toutes)
    "dv": 0,   # Carburant (tous)
    "ev": 0,   # Kilométrage (tous)
    "fv": 8,   # Filtre supplémentaire
    "genre": 0,
    "pp": 0,
    "localisation": 0,
    "pmin": 0,
    "pmax": 0
}

url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
print(f"URL de recherche : {url}")

def scrape_cars(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        cars = []

        for car_div in soup.find_all('div', id='rptregion'):
            title = car_div.find('div', id='titre').text.strip() if car_div.find('div', id='titre') else "N/A"

            if "Corolla" in title:
                price_div = car_div.find('div', id='prix')
                price = price_div.text.strip() if price_div else "N/A"

                try:
                    price = float(price.replace('MRU', '').replace(',', '').strip())
                except ValueError:
                    price = float('inf')

                image_url = car_div.find('img')['src'] if car_div.find('img') else "N/A"
                image_url = f"https://www.voursa.com{image_url}" if image_url != "N/A" else "N/A"

                link = car_div.find_parent('a')['href'] if car_div.find_parent('a') else "N/A"
                link = f"https://www.voursa.com{link}" if link != "N/A" else "N/A"

                cars.append({
                    'Title': title,
                    'Price': price,
                    'Image URL': image_url,
                    'Link': link
                })

        sorted_cars = sorted(cars, key=lambda x: x['Price'])

        top_10_corolla = sorted_cars[:10]

        return top_10_corolla
    else:
        print(f"Échec de la récupération du site. Code de statut : {response.status_code}")
        return []

cars = scrape_cars(url)

if cars:
    json_output = json.dumps(cars, ensure_ascii=False, indent=4)
    print("\nRésultats de la recherche (10 premières Corolla) :")
    print(json_output)
else:
    print("Aucune voiture Corolla trouvée.")