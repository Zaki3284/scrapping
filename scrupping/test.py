import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

url = "https://www.voursa.com/annonces.cfm?pdtid=356442&adtre=2017%20TOYOTA%20COROLLA"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1').text.strip() if soup.find('h1') else "N/A"

    price_div = soup.find('div', id='prix')
    price = price_div.text.strip() if price_div else "N/A"

    location_div = soup.find('div', id='localisation')
    location = location_div.find('span', class_='valued').text.strip() if location_div else "N/A"

    details_div = soup.find('div', id='details_category')
    details = {}
    if details_div:
        for span in details_div.find_all('span', class_='labeld'):
            key = span.text.strip().replace(':', '') 
            value = span.find_next('span', class_='valued').text.strip()
            details[key] = value

    desktop_path = "/Users/javaarhmeimed/desktop/voursa_car_details.pdf"
    c = canvas.Canvas(desktop_path, pagesize=letter)

    c.setFont("Helvetica", 12)

    y = 750  
    c.drawString(50, y, f"Title: {title}")
    y -= 20
    c.drawString(50, y, f"Price: {price}")
    y -= 20
    c.drawString(50, y, f"Location: {location}")
    y -= 20
    y -= 15
    y -= 10  

    for key, value in details.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    c.save()

    print(f"Scraping completed and PDF saved to {desktop_path}.")
else:
    print(f"Failed to retrieve the website. Status code: {response.status_code}")  