from django.db import models
from django.contrib.auth.models import User, AbstractUser
from ckeditor.fields import RichTextField
# Create your models here.

class TheLoai(models.Model):
    ten = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return str([self.ten, self.slug])

class SanPham(models.Model):
    the_loai = models.ForeignKey(TheLoai, on_delete=models.CASCADE, default=1)
    ten = models.CharField(max_length=300, null=True, blank=False)
    gia = models.IntegerField(blank=False)
    hinh = models.ImageField(null=True, blank=True)
    khuyen_mai = models.BooleanField(default=False) 
    gia_km = models.IntegerField(blank=True, null=True)
    mo_ta = RichTextField(default='', blank=True)
    hinh_phu_1 = models.ImageField(null=True, blank=True)
    hinh_phu_2 = models.ImageField(null=True, blank=True)
    hinh_phu_3 = models.ImageField(null=True, blank=True) 
    hinh_phu_4 = models.ImageField(null=True, blank=True)
    
    
    def __str__(self):
        return self.ten
    
    @property
    def ImageURL(self):
        try:
            url = self.hinh.url
        except:
            url = ''
        return url


class GioHang(models.Model):
    khach_hang = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    ngay_dat = models.DateTimeField(auto_now_add=True)
    ten = models.CharField(max_length=300, null=True, blank=False)
    hoan_thanh = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str('Giỏ hàng có stt ' + str(self.id) + ' của ' + self.ten)
    

class MucGioHang(models.Model):
    san_pham = models.ForeignKey(SanPham, on_delete=models.SET_NULL, blank=True, null=True)
    gio_hang = models.ForeignKey(GioHang, on_delete=models.SET_NULL, blank=True, null=True)
    so_luong = models.IntegerField(default=0, null=True, blank=True)
    ngay_them = models.DateTimeField(auto_now_add=True)
    kich_thuoc = models.IntegerField(default=37)
    
    def tinh_tong_gia_cua_tung_muc(self):
        if self.san_pham.gia_km: 
            tong_gia = self.san_pham.gia_km * self.so_luong
        else:
            tong_gia = self.san_pham.gia * self.so_luong
        return tong_gia
    
    def __str__(self):
        return str('Mục ' + str(self.id) + ' ' + str(self.gio_hang))
        

class DiaChiGiaoHang(models.Model):
    khach_hang = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    gio_hang = models.ForeignKey(GioHang, on_delete=models.SET_NULL, blank=True, null=True)
    thanh_pho = models.CharField(max_length=300, null=True)
    quan = models.CharField(max_length=300, null=True)
    phuong = models.CharField(max_length=300, null=True)
    dia_chi = models.CharField(max_length=300, null=True)
    sdt = models.CharField(max_length=300, null=True)
    ngay_giao = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=300, null=True)
    ten_nguoi_nhan = models.CharField(max_length=300, null=True)
    def __str__(self):
        return str(self.dia_chi)

class Profile(models.Model):
    khach_hang = models.OneToOneField(User, on_delete=models.CASCADE)
    ho_ten = models.CharField(max_length=300, null=True, blank=True)
    ngay_sinh = models.DateField(null=True, blank=True)
    sdt = models.CharField(max_length=20, blank=True, null=True)
    hinh = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.khach_hang)
    
    @property
    def ImageURL(self):
        try:
            url = self.hinh.url
        except:
            url = '/static/images/user-avatar.png'
        return url
    
   