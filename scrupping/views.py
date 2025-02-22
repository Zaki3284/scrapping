from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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
    return redirect('login')  # توجيه المستخدم إلى صفحة تسجيل الدخول بعد تسجيل الخروج

# @login_required
def dashboard(request):
    return render(request, 'indexuser.html')
