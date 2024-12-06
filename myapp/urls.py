from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .models import CanHo
from .views import login_view, ApartmentDetailView, ResidentAPIView
from .views import CustomLogoutView
from django.urls import path, include
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

    path('api/can-ho/<int:pk>/', ApartmentDetailView.as_view(), name='apartment-detail'),

    path('can-ho/<int:id>/', views.apartment_detail, name='apartment_detail'),

    path('resident-list/', views.Resident, name='resident_list'),

    path('api/resident', ResidentAPIView.as_view(), name='resident_api'),
]