from django.urls import path
from django.contrib import admin
from . import views
from .views import register_view, login_view, logout_view, forgot_password_view,apple_finals, reset_password_view,loginview,restpass,makeup_list,accessoire_list,cars_list,houses_list,appel_offre_list,job_offers_list,apple_signin,phone_list,phones
# RegisterView, LoginView, LogoutView ,ForgotPasswordView, ResetPasswordView, signup_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='landing_page'),
    path('signup/', views.signup_page, name='signup'),
    path('signin/', views.loginview, name='loginn'),
    path('fp/', views.forgetpass, name='forgetpass'),
    path('rsp/', views.restpass, name='restpass'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('phones/', views.phones, name='phones'),
    
    path('apple-signin/', views.apple_signin, name='apple_signin'),
    path('apple-confirm/', views.apple_confirm, name='apple_confirm'),
    path('apple-final/', views.apple_final, name='apple_final'),
    path('apple-finals/', views.apple_finals, name='apple_finals'),
    
    # path('cars/', views.scrape_cars, name='scrape_cars'),
    # path('houses/', views.scrape_houses, name='scrape_houses'),
    # path('get_models/', views.get_models, name='get_models'),
    # path('search_cars/', views.search_cars, name='search_cars'),
    # path('car_selection/', views.car_selection, name='car_selection'),
    
    path('makeup/', views.makeup_list, name='product_list'),
    path('accessoire/', views.accessoire_list, name='accessoire_list'),
    path('cars/', views.cars_list, name='cars_list'),
    path('houses/', views.houses_list, name='houses_list'),
    # path('houses2/', views.houses2_list, name='houses2_list'),
    path('appel_offre/', views.appel_offre_list, name='appel_offre_list'),
    path('job_offers/', views.job_offers_list, name='job_offers_list'),
    path('phone/', views.phone_list, name='phone_list'),
    
    
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    # path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', reset_password_view, name='reset_password'),
]
