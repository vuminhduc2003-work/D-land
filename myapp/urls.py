from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .models import CanHo
from .views import login_view
from .views import CustomLogoutView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApartmentAPIView
urlpatterns = [
    path('', views.index, name='index'),  # Trang chủ của ứng dụng myapp

    path('register/', views.register, name='register'),

    path("login/", login_view, name="login"),


    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('/home', views.home, name='home'),  # Trang chủ

    path('/dashboard/apartment', views.apartment_view, name='apartment_view'),


    path('api/can-ho', ApartmentAPIView.as_view(), name='apartment_list'),


]