from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

from unidecode import unidecode

# Create your views here.

# Hiển thị Trang home.html
def home(request):
    sanpham_list = SanPham.objects.all()
    theloai_list = TheLoai.objects.all()

    # list sản phẩm khuyến mãi
    sanpham_km_list = SanPham.objects.filter(khuyen_mai = True).order_by('-id')[:5]

    context = {'theloai_list' : theloai_list,
               'sanpham_list' : sanpham_list,
               'sanpham_km_list' : sanpham_km_list,}
    return render(request, "app/home.html", context)

# đăng nhập
def login_user(request):
    theloai_list = TheLoai.objects.all()
    context = {'theloai_list' : theloai_list} 

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Bạn đã đăng nhập thành công.")
            return redirect('home')
        
        else:
            messages.error(request, "Đăng nhập sai mật khẩu hoặc tên tài khoản!!! Vui lòng đăng nhập lại")
            return redirect('login_user')
        
    return render(request, "app/login.html", context)

# đăng xuất
def logout_user(request):
    logout(request)
    messages.success(request, "Bạn đã đăng xuất thành công")
    return redirect('home')
    
# đăng ký tk
def register_user(request):
    theloai_list = TheLoai.objects.all()
    context = {'theloai_list' : theloai_list} 

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2: 
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Tên đăng nhập đã tồn tại!!! Vui lòng nhập lại tên đăng nhập khác.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Tạo tài khoản thành công')
                return redirect('login_user')
        else: 
            messages.error(request, 'Xác thực mật khẩu không đúng!!! Vui lòng kiểm tra lại.')

    return render(request, "app/register.html", context)

# Hiển thị Trang sản phẩm theo thể loại 
def category(request, tl):
    tl = unidecode(tl).lower().replace(' ', '-') 
    theloai = TheLoai.objects.get(slug = tl)
    # list sản phẩm theo từng thể loại
    sanpham_list = SanPham.objects.filter(the_loai = theloai)
    
    # tính năng lọc 
    sap_xep = request.GET.get('sort-by')
    if sap_xep == 'tang':
        sanpham_list = sanpham_list.order_by('gia')
    elif sap_xep == 'giam':
        sanpham_list = sanpham_list.order_by('-gia')
    elif sap_xep == 'a-z':
        sanpham_list = sanpham_list.order_by('ten')
    elif sap_xep == 'z-a':
        sanpham_list = sanpham_list.order_by('-ten')

    theloai_list = TheLoai.objects.all()
    context = {'theloai_list' : theloai_list,
               'sanpham_list' : sanpham_list,
               'theloai' : theloai}   
    return render(request, "app/category.html", context)

# Tính năng thêm vào giỏ hàng 
def them_vao_gio_hang(request):
    if request.method == "POST":
        san_pham_id = request.POST.get('san_pham_id')
        so_luong = request.POST.get('so_luong')

        gio_hang, created = GioHang.objects.get_or_create(khach_hang=request.user, hoan_thanh=False, ten=request.user)
        san_pham = SanPham.objects.get(pk=san_pham_id)

        muc_gio_hang, created = MucGioHang.objects.get_or_create(san_pham=san_pham, gio_hang=gio_hang)
        
        muc_gio_hang.so_luong = muc_gio_hang.so_luong + int(so_luong) 
        muc_gio_hang.save()

        return JsonResponse({'success' : True})
    return JsonResponse({'success' : False})


# Hiển thị Trang Cart.html
def cart(request):
    theloai_list = TheLoai.objects.all()
    gio_hang = GioHang.objects.filter(khach_hang=request.user, hoan_thanh=False).first()
    gia_tri_gio_hang = 0

    if gio_hang: 
        muc_gio_hang = MucGioHang.objects.filter(gio_hang=gio_hang)
        for muc in muc_gio_hang:
            muc.tong_gia_cua_tung_muc = muc.tinh_tong_gia_cua_tung_muc()
            gia_tri_gio_hang += muc.tong_gia_cua_tung_muc    
    else:
        muc_gio_hang = None
    
    context = {'muc_gio_hang' : muc_gio_hang, 
               'theloai_list' : theloai_list,
               'gia_tri_gio_hang' : gia_tri_gio_hang}
    return render(request, 'app/cart.html', context)

# tính năng cập nhật mục giỏ hàng 
def cap_nhat_muc_gio_hang(request):
    if request.method == 'POST': 
        san_pham_id = request.POST.get('san_pham_id')
        so_luong = request.POST.get('so_luong')

        muc_gio_hang = MucGioHang.objects.get(san_pham=san_pham_id, gio_hang__khach_hang = request.user, gio_hang__hoan_thanh=False)
        muc_gio_hang.so_luong = so_luong
        muc_gio_hang.save()

        return JsonResponse({'success' : True})
    return JsonResponse({'success' : False})

# tính năng xóa mục giỏ hàng 
def xoa_muc_gio_hang(request):
    if request.method == 'POST':
        muc_id = request.POST.get('muc_id')
        muc_id = MucGioHang.objects.get(pk=muc_id)
        muc_id.delete()

        return JsonResponse({'success' : True})
    return JsonResponse({'success' : False})

# tính năng lấy tổng số lượng sản phẩm trong giỏ hàng để hiện lên icon Giỏ Hàng
def lay_so_luong_san_pham_trong_gio_hang(user):
    if user.is_authenticated:
        gio_hang = GioHang.objects.filter(khach_hang=user, hoan_thanh=False).first()
        if gio_hang:
            muc_gio_hang = MucGioHang.objects.filter(gio_hang=gio_hang)
            tong_san_pham = 0
            for muc in muc_gio_hang:
                tong_san_pham += muc.so_luong
            return tong_san_pham
    return 0
        
# Hiển thị trang checkout
def checkout(request):
    return render(request, 'app/checkout.html')
                

