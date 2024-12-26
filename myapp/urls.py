from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import login_view, ResidentViewSet, apartment_list
from .views import CustomLogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='index'),  # Trang chủ của ứng dụng myapp

    path('register/', views.register, name='register'),

    path('', login_view, name="login"),

    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('Notification', views.Notification, name='notification'),

    path('dashboard', views.dashboard, name='dashboard'),

    path('home', views.home, name='home'),

    path('', include('myapp.url_api')),  # Các URL khác cho ứng dụng của bạn

    path('residents/', views.resident_list, name='resident-list'),

    path('apartment', apartment_list, name='apartment_list'),

    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)