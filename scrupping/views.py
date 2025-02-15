from django.shortcuts import render


def login_view(request):
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/signup.html')

def forgetpass(request):
    return render(request, 'auth/ForgetPassword.html')

def landing_page(request):
    return render(request, 'auth/landing.html') 

def index(request):
    return render(request, 'index.html')

def logout_view(request):
    return render(request, 'auth/logout.html')

def dashboard(request):
    return render(request, 'indexuser.html')