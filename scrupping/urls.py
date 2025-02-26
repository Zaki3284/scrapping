from django.urls import path
from . import views
from .views import RegisterView, LoginView, LogoutView ,ForgotPasswordView, ResetPasswordView

urlpatterns = [
    # path('', views.index, name='landing_page'),
    # path('login/', views.login_view, name='login'),
    # path('register/', views.register_view, name='register'),
    # path('forgetpass/', views.forgetpass, name='forgetpass'),
    # path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cars/', views.scrape_cars, name='scrape_cars'),
    path('houses/', views.scrape_houses, name='scrape_houses'),
    path('get_models/', views.get_models, name='get_models'),
    path('search_cars/', views.search_cars, name='search_cars'),
    path('car_selection/', views.car_selection, name='car_selection'),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
]
