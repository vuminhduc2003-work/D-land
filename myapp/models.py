
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)  # Link to user account
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)  # Valid datetime
    apartment = models.ForeignKey('Apartment', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name

class FamilyMember(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    relationship = models.CharField(max_length=50, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Child', 'Child'), ('Spouse', 'Spouse'), ('Other', 'Other')])
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    primary_resident = models.ForeignKey('Resident', on_delete=models.CASCADE, related_name='family_members')

    def __str__(self):
        return f'{self.full_name} ({self.relationship}) of {self.primary_resident.full_name}'

class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    apartment_code = models.CharField(max_length=20, unique=True)
    building = models.CharField(max_length=50)
    floor_number = models.IntegerField()
    area = models.DecimalField(max_digits=5, decimal_places=2)  # m²
    apartment_orientation = models.CharField(max_length=20, choices=[
        ('East', 'East'),
        ('West', 'West'),
        ('South', 'South'),
        ('North', 'North'),
        ('Southeast', 'Southeast'),
        ('Southwest', 'Southwest'),
        ('Northeast', 'Northeast'),
        ('Northwest', 'Northwest')
    ])  # Apartment orientation
    status = models.CharField(max_length=20, choices=[('Vacant', 'Vacant'), ('Rented', 'Rented'), ('Sold', 'Sold'), ('Maintenance', 'Maintenance')], default='Vacant')
    residents = models.ManyToManyField(Resident, related_name='apartments', blank=True)  # Updated related_name to 'apartments'

    def __str__(self):
        return f'{self.apartment_code} - {self.building}'

class Room(models.Model):
    room_code = models.CharField(max_length=20, unique=True)  # Room code
    room_name = models.CharField(max_length=100)             # Room name
    room_type = models.CharField(max_length=50, choices=[
        ('Living Room', 'Living Room'),
        ('Bedroom', 'Bedroom'),
        ('Kitchen', 'Kitchen'),
        ('Bathroom', 'Bathroom'),
    ])  # Room type
    area = models.DecimalField(max_digits=5, decimal_places=2)  # Room area
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='rooms')  # Link to apartment

    def __str__(self):
        return f'{self.room_name} - {self.room_code}'

class Facility(models.Model):
    name = models.CharField(max_length=50)  # Facility name
    description = models.TextField(null=True, blank=True)   # Facility description (e.g., air conditioning, internet,...)

    def __str__(self):
        return self.name

class ServiceFee(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=50, choices=[('Electricity', 'Electricity'), ('Water', 'Water'), ('Management Fee', 'Management Fee')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.fee_type} - {self.resident.full_name} - {self.month.strftime("%m/%Y")}'

class MaintenanceRequest(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Processing', 'Processing'), ('Completed', 'Completed')], default='Processing')

    def __str__(self):
        return f'{self.title} - {self.resident.full_name}'

class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(Resident)

    def __str__(self):
        return self.title

class EntryExitHistory(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    exit_time = models.DateTimeField(null=True, blank=True)
    entry_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.resident.full_name} - {self.entry_time} -> {self.exit_time}'

class RentalAgreement(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Contract: {self.resident.full_name} - {self.apartment.apartment_code}'
































# from django.db import models
# from django.utils.timezone import now
#
# # Create your models here.
#
#
# from django.db import models
# from django.contrib.auth.models import User
#
# class CuDan(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Kết nối với tài khoản người dùng
#     ho_ten = models.CharField(max_length=100)
#     so_dien_thoai = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(unique=True)
#     ngay_sinh = models.DateField(null=True, blank=True)
#     gioi_tinh = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], default='Nam')
#     dia_chi = models.CharField(max_length=255)
#     created_at = models.DateTimeField(default=now)  # datetime hợp lệ
#     can_ho = models.ForeignKey('CanHo', on_delete=models.SET_NULL, null=True)
#
#     def __str__(self):
#         return self.ho_ten
#
# class NguoiNha(models.Model):
#     ho_ten = models.CharField(max_length=100)
#     ngay_sinh = models.DateField()
#     gioi_tinh = models.CharField(max_length=10, choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], default='Nam')
#     quan_he = models.CharField(max_length=50, choices=[('Cha', 'Cha'), ('Mẹ', 'Mẹ'), ('Con', 'Con'), ('Vợ/Chồng', 'Vợ/Chồng'), ('Khác', 'Khác')])
#     so_dien_thoai = models.CharField(max_length=15, null=True, blank=True)
#     cu_dan_chinh = models.ForeignKey('CuDan', on_delete=models.CASCADE, related_name='nguoi_nha')
#
#     def __str__(self):
#         return f'{self.ho_ten} ({self.quan_he}) của {self.cu_dan_chinh.ho_ten}'
#
#
# class CanHo(models.Model):
#     id = models.AutoField(primary_key=True)
#
#     ma_can_ho = models.CharField(max_length=20, unique=True)
#     toa_nha = models.CharField(max_length=50)
#     so_tang = models.IntegerField()
#     dien_tich = models.DecimalField(max_digits=5, decimal_places=2)  # m²
#     huong_can_ho = models.CharField(max_length=20, choices=[
#         ('Đông', 'Đông'),
#         ('Tây', 'Tây'),
#         ('Nam', 'Nam'),
#         ('Bắc', 'Bắc'),
#         ('Đông Nam', 'Đông Nam'),
#         ('Tây Nam', 'Tây Nam'),
#         ('Đông Bắc', 'Đông Bắc'),
#         ('Tây Bắc', 'Tây Bắc')
#     ])  # Hướng căn hộ
#     trang_thai = models.CharField(max_length=20, choices=[('Trống', 'Trống'), ('Đã thuê', 'Đã thuê'), ('Đã bán', 'Đã bán'), ('Bảo trì', 'Bảo trì')], default='Trống')
#     cu_dan = models.ManyToManyField(CuDan, related_name='ds_can_ho', blank=True)  # Đổi related_name thành 'ds_can_ho'
#
#     def __str__(self):
#         return f'{self.ma_can_ho} - {self.toa_nha}'
#
# class Phong(models.Model):
#     ma_phong = models.CharField(max_length=20, unique=True)  # Mã phòng
#     ten_phong = models.CharField(max_length=100)             # Tên phòng
#     loai_phong = models.CharField(max_length=50, choices=[
#         ('Phòng khách', 'Phòng khách'),
#         ('Phòng ngủ', 'Phòng ngủ'),
#         ('Phòng bếp', 'Phòng bếp'),
#         ('Phòng tắm', 'Phòng tắm'),
#     ])  # Loại phòng
#     dien_tich = models.DecimalField(max_digits=5, decimal_places=2)  # Diện tích phòng
#     can_ho = models.ForeignKey(CanHo, on_delete=models.CASCADE, related_name='phong')  # Liên kết với căn hộ
#
#     def __str__(self):
#         return f'{self.ten_phong} - {self.ma_phong}'
#
# class TienNghi(models.Model):
#     ten_tien_nghi = models.CharField(max_length=50)  # Tên tiện nghi
#     mo_ta = models.TextField(null=True, blank=True)   # Mô tả tiện nghi (Ví dụ: máy lạnh, internet,...)
#
#     def __str__(self):
#         return self.ten_tien_nghi
#
#
# class PhiDichVu(models.Model):
#     cu_dan = models.ForeignKey(CuDan, on_delete=models.CASCADE)
#     loai_phi = models.CharField(max_length=50, choices=[('Điện', 'Điện'), ('Nước', 'Nước'), ('Phí quản lý', 'Phí quản lý')])
#     so_tien = models.DecimalField(max_digits=10, decimal_places=2)
#     thang = models.DateField()
#     da_thanh_toan = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.loai_phi} - {self.cu_dan.ho_ten} - {self.thang.strftime("%m/%Y")}'
#
# class YeuCauBaoTri(models.Model):
#     cu_dan = models.ForeignKey(CuDan, on_delete=models.CASCADE)
#     tieu_de = models.CharField(max_length=100)
#     noi_dung = models.TextField()
#     ngay_tao = models.DateTimeField(auto_now_add=True)
#     trang_thai = models.CharField(max_length=20, choices=[('Đang xử lý', 'Đang xử lý'), ('Đã hoàn thành', 'Đã hoàn thành')], default='Đang xử lý')
#
#     def __str__(self):
#         return f'{self.tieu_de} - {self.cu_dan.ho_ten}'
#
#
# class ThongBao(models.Model):
#     tieu_de = models.CharField(max_length=100)
#     noi_dung = models.TextField()
#     ngay_gui = models.DateTimeField(auto_now_add=True)
#     nguoi_nhan = models.ManyToManyField(CuDan)
#
#     def __str__(self):
#         return self.tieu_de
#
#
# class LichSuRaVao(models.Model):
#     cu_dan = models.ForeignKey(CuDan, on_delete=models.CASCADE)
#     thoi_gian_ra = models.DateTimeField(null=True, blank=True)
#     thoi_gian_vao = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.cu_dan.ho_ten} - {self.thoi_gian_vao} -> {self.thoi_gian_ra}'
#
#
# class HopDongThue(models.Model):
#     cu_dan = models.ForeignKey(CuDan, on_delete=models.CASCADE)
#     can_ho = models.ForeignKey(CanHo, on_delete=models.CASCADE)
#     ngay_bat_dau = models.DateField()
#     ngay_ket_thuc = models.DateField()
#     gia_thue = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def __str__(self):
#         return f'Hợp đồng: {self.cu_dan.ho_ten} - {self.can_ho.ma_can_ho}'
