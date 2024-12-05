from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import RegisterForm
from django.contrib.auth.views import LoginView,  LogoutView
from rest_framework import viewsets, status
from .models import CanHo
from .serializers import CanHoSerializer


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
        canhos = CanHo.objects.all()
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
