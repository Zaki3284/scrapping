from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgetpass/', views.forgetpass, name='forgetpass'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
