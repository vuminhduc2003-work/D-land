from http.client import responses
from urllib import request

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import RegisterForm
from django.contrib.auth.views import LoginView,  LogoutView
from rest_framework import viewsets, status
from .models import Resident, FamilyMember, Apartment, Room, Facility, ServiceFee, MaintenanceRequest, Notification, EntryExitHistory, RentalAgreement
from .serializers import ResidentSerializer, FamilyMemberSerializer, ApartmentSerializer, RoomSerializer, FacilitySerializer, ServiceFeeSerializer, MaintenanceRequestSerializer, NotificationSerializer, EntryExitHistorySerializer, RentalAgreementSerializer

def is_admin(user):
    return user.is_superuser
def index(request):
    return render(request, 'myapp/introduce.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tài khoản đã được tạo thành công! Bạn có thể đăng nhập ngay bây giờ.')
            return redirect('login')
        else:
            messages.error(request, "Có lỗi xảy ra, vui lòng kiểm tra lại thông tin.")
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Đăng nhập thành công!")
            return redirect('dashboard')
        else:
            messages.error(request,"Tên đăng nhập hoặc mật khẩu không đúng!")
    return render(request, 'myapp/login.html')

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse('login')
def home(request):
    return render(request, 'myapp/home.html')


@login_required
@user_passes_test(is_admin, login_url='/login')
def dashboard(request):
    # Nếu người dùng không phải admin, họ sẽ bị chuyển hướng tới trang đăng nhập
    return render(request, 'dashboard2.html', {'title': 'Dashboard'})

def resident_list(request):
    return render(request, 'myapp/dashboard/Resident/Resident.html')

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer

class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

class ServiceFeeViewSet(viewsets.ModelViewSet):
    queryset = ServiceFee.objects.all()
    serializer_class = ServiceFeeSerializer

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class EntryExitHistoryViewSet(viewsets.ModelViewSet):
    queryset = EntryExitHistory.objects.all()
    serializer_class = EntryExitHistorySerializer

class RentalAgreementViewSet(viewsets.ModelViewSet):
    queryset = RentalAgreement.objects.all()
    serializer_class = RentalAgreementSerializer
