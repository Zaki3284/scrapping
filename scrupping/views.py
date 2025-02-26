from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import date
from itertools import islice
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from selenium import webdriver
import time
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import *
import requests
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from bs4 import BeautifulSoup
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.db.models.functions import Random
from .models import CustomUser
# from .serializers import CustomUserSerializer


def login_view(request):
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/signup.html')

def forgetpass(request):
    return render(request, 'auth/password_reset.html')  # تغيير الاسم ليتبع المعايير

def landing_page(request):
    return render(request, 'auth/landing.html')

def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')  

def dashboard(request):
    return render(request, 'indexuser.html')



def scrape_cars(request):
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

            image_url = car_div.find('img')['src'] if car_div.find('img') else "N/A"
            image_url = f"https://www.voursa.com{image_url}" if image_url != "N/A" else "N/A"

            link = car_div.find_parent('a')['href'] if car_div.find_parent('a') else "N/A"
            link = f"https://www.voursa.com{link}" if link != "N/A" else "N/A"

            cars.append({
                'Title': title,
                'Price': price,
                'Image_URL': image_url,  
                'Link': link
            })

        sorted_cars = sorted(cars, key=lambda x: x['Price'])
        cheapest_cars = sorted_cars[:10]

        for car in cheapest_cars:
            print(f"Image URL: {car['Image_URL']}")

        context = {
            'cars': cheapest_cars
        }
        return render(request, 'car_list.html', context)
    else:
        return render(request, 'error.html', {'error': f"Failed to retrieve the website. Status code: {response.status_code}"})
    
    
def scrape_houses(request):
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

            # Extract link
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

        context = {
            'houses': cheapest_houses
        }
        return render(request, 'house_list.html', context)
    else:
        return render(request, 'error1.html', {'error': f"Failed to retrieve the website. Status code: {response.status_code}"})
    
    
# -------------------------start ----------------------------
marque_mapping = {"Toyota": 1, "Mercedes": 2, "Hyundai": 4}
models_by_brand = {
    "Toyota": {"Corolla": 24, "avensus": 20, "rav4": 28, "hilux": 25, "tx": 27},
    "Hyundai": {"accent": 118, "Elantra": 119, "Santa fe": 124, "sonata": 125},
    "Mercedes": {} 
}

def scrape_cars(av, bv=0):
    url = f"https://www.voursa.com/Index.cfm?gct=1&sct=11&gv=1&av={av}&bv={bv}&cv=0&dv=0&ev=0&fv=0&genre=0&pp=0&localisation=0&pmin=0&pmax=0"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    cars = []
    for car_div in soup.find_all('div', id='rptregion'):
        title = car_div.find('div', id='titre').text.strip() if car_div.find('div', id='titre') else "N/A"
        price = car_div.find('div', id='prix').text.strip().replace('MRU', '').replace(',', '').strip()
        price = float(price) if price.isdigit() else float('inf')
        image_url = f"https://www.voursa.com{car_div.find('img')['src']}" if car_div.find('img') else "N/A"
        link = f"https://www.voursa.com{car_div.find_parent('a')['href']}" if car_div.find_parent('a') else "N/A"
        cars.append({'Title': title, 'Price': price, 'Image_URL': image_url, 'Link': link})
    return sorted(cars, key=lambda x: x['Price'])[:10]

def car_selection(request):
    return render(request, 'car_selection.html', {"brands": marque_mapping.keys()})

def get_models(request):
    brand = request.GET.get('brand')
    models = models_by_brand.get(brand, {})
    return JsonResponse(models, safe=False)

def search_cars(request):
    brand = request.GET.get('brand')
    model = request.GET.get('model', '')
    av = marque_mapping.get(brand, 0)
    bv = models_by_brand.get(brand, {}).get(model, 0)
    cars = scrape_cars(av, bv)
    return JsonResponse(cars, safe=False)
# -------------------------finish ----------------------------


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

       
        reset_link = f" http://127.0.0.1:8000/reset-password/{uid}/{token}/"

       
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            'laveapp24@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        return render(request, 'reset-password.html')

    def post(self, request, uidb64, token):
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({'error': 'Invalid user or token'}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)