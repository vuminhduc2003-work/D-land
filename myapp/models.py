from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User

class CuDan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Kết nối với tài khoản người dùng
    ho_ten = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    ngay_sinh = models.DateField(null=True, blank=True)
    gioi_tinh = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], default='Nam')
    dia_chi = models.CharField(max_length=255)
    ngay_dang_ky = models.DateTimeField(auto_now_add=True)
    can_ho = models.ForeignKey('CanHo', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ho_ten

class NguoiNha(models.Model):
    ho_ten = models.CharField(max_length=100)
    ngay_sinh = models.DateField()
    gioi_tinh = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], default='Nam')
    quan_he = models.CharField(max_length=50, choices=[('Cha', 'Cha'), ('Mẹ', 'Mẹ'), ('Con', 'Con'), ('Vợ/Chồng', 'Vợ/Chồng'), ('Khác', 'Khác')])
    so_dien_thoai = models.CharField(max_length=15, null=True, blank=True)
    cu_dan_chinh = models.ForeignKey('CuDan', on_delete=models.CASCADE, related_name='nguoi_nha')

    def __str__(self):
        return f'{self.ho_ten} ({self.quan_he}) của {self.cu_dan_chinh.ho_ten}'

class ChuSoHuu(models.Model):
    ho_ten = models.CharField(max_length=100)  # Họ tên chủ sở hữu
    so_dien_thoai = models.CharField(max_length=15)  # Số điện thoại
    email = models.EmailField()  # Email

    def __str__(self):
        return self.ho_ten


class CanHo(models.Model):
    chu_so_huu = models.ManyToManyField(ChuSoHuu, related_name='can_ho', blank=True)  # Liên kết nhiều chủ sở hữu/cư dân
    ma_can_ho = models.CharField(max_length=20, unique=True)
    toa_nha = models.CharField(max_length=50)
    so_tang = models.IntegerField()
    dien_tich = models.DecimalField(max_digits=5, decimal_places=2)  # m²
    huong_can_ho = models.CharField(max_length=20, choices=[
        ('Đông', 'Đông'),
        ('Tây', 'Tây'),
        ('Nam', 'Nam'),
        ('Bắc', 'Bắc'),
        ('Đông Nam', 'Đông Nam'),
        ('Tây Nam', 'Tây Nam'),
        ('Đông Bắc', 'Đông Bắc'),
        ('Tây Bắc', 'Tây Bắc')
    ])  # Hướng căn hộ

    trang_thai = models.CharField(max_length=20, choices=[('Trống', 'Trống'), ('Đã thuê', 'Đã thuê'),('Đã bán','Đã bán'),('Bảo trì','Bảo trì')], default='Trống')


    def __str__(self):
        return f'{self.ma_can_ho} - {self.toa_nha}'

class Phong(models.Model):
    ma_phong = models.CharField(max_length=20, unique=True)  # Mã phòng
    ten_phong = models.CharField(max_length=100)             # Tên phòng
    loai_phong = models.CharField(max_length=50, choices=[
        ('Phòng khách', 'Phòng khách'),
        ('Phòng ngủ', 'Phòng ngủ'),
        ('Phòng bếp', 'Phòng bếp'),
        ('Phòng tắm', 'Phòng tắm'),
    ])  # Loại phòng
    dien_tich = models.DecimalField(max_digits=5, decimal_places=2)  # Diện tích phòng
    can_ho = models.ForeignKey(CanHo, on_delete=models.CASCADE, related_name='phong')  # Liên kết với căn hộ

    def __str__(self):
        return f'{self.ten_phong} - {self.ma_phong}'

class TienNghi(models.Model):
    ten_tien_nghi = models.CharField(max_length=50)  # Tên tiện nghi
    mo_ta = models.TextField(null=True, blank=True)   # Mô tả tiện nghi (Ví dụ: máy lạnh, internet,...)

    def __str__(self):
        return self.ten_tien_nghi


class PhiDichVu(models.Model):
    cu_dan = models.ForeignKey(CuDan, on_delete=models.CASCADE)
    loai_phi = models.CharField(max_length=50, choices=[('Điện', 'Điện'), ('Nước', 'Nước'), ('Phí quản lý', 'Phí quản lý')])
    so_tien = models.DecimalField(max_digits=10, decimal_places=2)
    thang = models.DateField()
    da_thanh_toan = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.loai_phi} - {self.cu_dan.ho_ten} - {self.thang.strftime("%m/%Y")}'

class YeuCauBaoTri(models.Model):
    cu_dan = models.ForeignKey(CuDan, on_delete=models.CASCADE)
    tieu_de = models.CharField(max_length=100)
    noi_dung = models.TextField()
    ngay_tao = models.DateTimeField(auto_now_add=True)
    trang_thai = models.CharField(max_length=20, choices=[('Đang xử lý', 'Đang xử lý'), ('Đã hoàn thành', 'Đã hoàn thành')], default='Đang xử lý')

    def __str__(self):
        return f'{self.tieu_de} - {self.cu_dan.ho_ten}'


class ThongBao(models.Model):
    tieu_de = models.CharField(max_length=100)
    noi_dung = models.TextField()
    ngay_gui = models.DateTimeField(auto_now_add=True)
    nguoi_nhan = models.ManyToManyField(CuDan)

    def __str__(self):
        return self.tieu_de


class LichSuRaVao(models.Model):
    cu_dan = models.ForeignKey(CuDan, on_delete=models.CASCADE)
    thoi_gian_ra = models.DateTimeField(null=True, blank=True)
    thoi_gian_vao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.cu_dan.ho_ten} - {self.thoi_gian_vao} -> {self.thoi_gian_ra}'


class HopDongThue(models.Model):
    cu_dan = models.ForeignKey(CuDan, on_delete=models.CASCADE)
    can_ho = models.ForeignKey(CanHo, on_delete=models.CASCADE)
    ngay_bat_dau = models.DateField()
    ngay_ket_thuc = models.DateField()
    gia_thue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Hợp đồng: {self.cu_dan.ho_ten} - {self.can_ho.ma_can_ho}'
