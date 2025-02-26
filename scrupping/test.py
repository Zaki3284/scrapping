import requests
from bs4 import BeautifulSoup
import json

marque_mapping = {
    "Toyota": 1,
    "mercedes": 2,
    "mitsibushi": 3,
    "hyndai": 4,
    "audi": 5,
}

modele_mapping = {
    "Corolla": 24, # <--24
    "avensus": 2,# <--20
    "rav4": 3,# <--28
    "hilux": 7,# <--25
    "tx": 9,# <--27
}

boite_vitesse_mapping = {
    "Manual": 1,
    "Automatic": 2,
}

carburant_mapping = {
    "Gasoil": 1,
    "Essence": 2,
}

annee_modele_mapping = {
    "2022": 2022,
    "2021": 2021,
    "2020": 2020,
    "2019": 2019,
    "2018": 2018,
    "2017": 2017,
    "2016": 2016,
    "2015": 2015,
    "2014": 2014,
    "2013": 2013,
    "2012": 2012,
    "2011": 2011,
    "2010": 2010
}

kilometrage_mapping = {
    "5000": 1,
    "10000": 2,
    "20000": 3,
    "50000": 4,
    "100000": 5,
    "150000": 6,
    "200000": 7,
    "300000": 8,
}

def get_user_input():
    print("Please enter the following details to search for cars:")
    marque = input("Marque (Brand): ")
    modele = input("Modele (Model): ")
    boite_vitesse = input("Boite vitesse (Gearbox): ")
    carburant = input("Carburant (Fuel): ")
    annee_modele = input("Année de modele (Year): ")
    kilometrage = input("Kilometrage (Mileage): ")

    return {
        "marque": marque,
        "modele": modele,
        "boite_vitesse": boite_vitesse,
        "carburant": carburant,
        "annee_modele": annee_modele,
        "kilometrage": kilometrage
    }

def construct_url(user_input):
    base_url = "https://www.voursa.com/index.cfm"
    params = {
        "gct": 1,  # Category (Cars)
        "sct": 11,  # Subcategory
        "gv": 1,  # Default value for gv
        "av": marque_mapping.get(user_input["marque"]),  # Marque (Brand)
        "bv": modele_mapping.get(user_input["modele"]),  # Modele (Model)
        "cv": annee_modele_mapping.get(user_input["annee_modele"]),  # Année de modele (Year)
        "dv": carburant_mapping.get(user_input["carburant"]),  # Carburant (Fuel)
        "ev": boite_vitesse_mapping.get(user_input["boite_vitesse"]),  # Boite vitesse (Gearbox)
        "fv": kilometrage_mapping.get(user_input["kilometrage"],0),  # Kilometrage (Mileage)
        "genre": 0,
        "pp": 0,
        "localisation": 0,
        "pmin": 0,
        "pmax": 0
    }
    
    for key, value in params.items():
        if value is None:
            params[key] = 0

    url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return url

def scrape_cars(url):
    response = requests.get(url)

    if response.status_code == 200:
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

        cheapest_cars = sorted_cars[:10]

        return cheapest_cars
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return []

if __name__ == "__main__":
    user_input = get_user_input()

    url = construct_url(user_input)
    print(f"Constructed URL: {url}")

    cars = scrape_cars(url)

    if cars:
        json_output = json.dumps(cars, ensure_ascii=False, indent=4)
        print("\nSearch Results (JSON Format):")
        print(json_output)
    else:
        print("No cars found matching the criteria.")
        
"https://www.voursa.com/index.cfm?gct=1&sct=11&gv=1&av=1&bv=28&cv=0&dv=0&ev=0&fv=0&genre=0&pp=0&localisation=0&pmin=0&pmax=0"
" https://www.voursa.com/index.cfm?gct=1&sct=11&gv=1&av=1&bv=24&cv=None&dv=None&ev=None&fv=0&genre=0&pp=0&localisation=0&pmin=0&pmax=0"