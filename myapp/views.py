from http.client import responses
from urllib import request

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import RegisterForm
from django.contrib.auth.views import LoginView,  LogoutView
from rest_framework import viewsets, status
from .models import CanHo, CuDan
from .serializers import CanHoSerializer, CuDanSerializer


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
            return redirect('home')
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

    return render(request, 'dashboard2.html', {'title': 'Dashboard'})


def apartment_view(request):
    return render(request, 'myapp/dashboard/Apartment/Apartment.html')

class ApartmentAPIView(APIView):

    def get(self, request):
        canhos = CanHo.objects.all()[:10]
        serializer = CanHoSerializer(canhos, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        print("Dữ liệu nhận được:", request.data)
        serializer = CanHoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Lỗi khi serialize:", serializer.errors)  # Log lỗi nếu có
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApartmentDetailView(APIView):
    def get(self, request, pk):
        try:
            canho = CanHo.objects.get(pk=pk)
            serializer = CanHoSerializer(canho)
            return Response(serializer.data)
        except CanHo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def put(self, request, pk):
        try:
            canho = CanHo.objects.get(pk=pk)
            serializer = CanHoSerializer(canho, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CanHo.DoesNotExist:
            return Response({"detail":"Apartment not found"},status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        canho = CanHo.objects.get(pk=pk)
        canho.delete()
        return Response({"detail":"Can Ho da duoc xoa"},status=status.HTTP_204_NO_CONTENT)


def apartment_detail(request, id):
    apartment = get_object_or_404(CanHo, id=id)
    return render(request, 'myapp/dashboard/Apartment/ApartmentDetail.html', {'apartment': apartment})

def Resident(request):
    return render(request, 'myapp/dashboard/Resident/Resident.html')

class ResidentAPIView(APIView):
    def get(self, request):
        try:
            residents = CuDan.objects.all()
            serializer = CuDanSerializer(residents, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def resident_list(request):
        residents = CanHo.objects.select_related('ma_can_ho').all()  # Sử dụng select_related để truy xuất căn hộ cùng lúc
        return render(request, 'myapp/dashboard/Resident/Resident.html', {'residents': residents})

    @csrf_exempt
    def post(self, request):
        serializer = CuDanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Lỗi khi serialize:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def Notification(request):
    return render(request, 'myapp/Website/navWeb/Notification.html')


