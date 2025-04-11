import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

#! with name and phone number

def get_owner_info(car_url):
    response = requests.get(car_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        owner_name = "N/A"
        owner_phone = "N/A"

        seller_info = soup.find('div', id='vendeur_t')
        if seller_info:
            vendinfo = seller_info.find_next('div', id='vendinfo')
            if vendinfo:
                lines = vendinfo.get_text(separator='\n').split('\n')
                for line in lines:
                    if "Nom :" in line:
                        owner_name = line.replace("Nom :", "").strip()
                    if "Téléphones:" in line:
                        owner_phone = line.replace("Téléphones:", "").strip()

        return owner_name, owner_phone
    else:
        return "N/A", "N/A"

url = "https://www.voursa.com/Index.cfm?gct=1&sct=11&gv=13"
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

        image_tag = car_div.find('img')
        image_url = image_tag['src'] if image_tag else "N/A"
        image_url = f"https://www.voursa.com{image_url}" if image_url != "N/A" else "N/A"

        link_tag = car_div.find_parent('a')
        link = link_tag['href'] if link_tag else "N/A"
        link = f"https://www.voursa.com{link}" if link != "N/A" else "N/A"

        owner_name, owner_phone = get_owner_info(link)

        cars.append({
            'Title': title,
            'Price': price,
            'Image URL': image_url,
            'Link': link,
            'Owner Name': owner_name,
            'Owner Phone': owner_phone
        })

    sorted_cars = sorted(cars, key=lambda x: x['Price'])

    cheapest_cars = sorted_cars[:10]
    cheapest_cars = sorted_cars[:10]

    desktop_path = "/Users/javaarhmeimed/desktop/cheapest_cars.pdf"
    c = canvas.Canvas(desktop_path, pagesize=letter)

    c.setFont("Helvetica", 12)

    y = 750

    for car in cheapest_cars:
        c.drawString(50, y, f"Title: {car['Title']}")
        y -= 20
        c.drawString(50, y, f"Price: {car['Price']} MRU" if car['Price'] != float('inf') else "Price: Undetermined")
        y -= 20
        c.drawString(50, y, f"Image URL: {car['Image URL']}")
        y -= 20
        c.drawString(50, y, f"Link: {car['Link']}")
        y -= 20
        c.drawString(50, y, f"Owner Name: {car['Owner Name']}")
        y -= 20
        c.drawString(50, y, f"Owner Phone: {car['Owner Phone']}")
        y -= 30

    c.save()

    print(f"Scraping completed and PDF saved to {desktop_path}.")
else:
    print(f"Failed to retrieve the website. Status code: {response.status_code}")