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
    sanpham_km_list = SanPham.objects.filter(khuyen_mai = True).order_by('-id')[:4]

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
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2: 
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Tên đăng nhập đã tồn tại!!! Vui lòng nhập lại tên đăng nhập khác.')
            else:
                user = User.objects.create_user(last_name=name, username=username, email=email, password=password1)
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
        kich_thuoc = request.POST.get('kich_thuoc', '37')

        gio_hang, created = GioHang.objects.get_or_create(khach_hang=request.user, hoan_thanh=False, ten=request.user)
        san_pham = SanPham.objects.get(pk=san_pham_id)

        muc_gio_hang, created = MucGioHang.objects.get_or_create(san_pham=san_pham, gio_hang=gio_hang, kich_thuoc=kich_thuoc)
        
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
        kich_thuoc = request.POST.get('kich_thuoc')
        muc_gio_hang = MucGioHang.objects.get(san_pham=san_pham_id, gio_hang__khach_hang = request.user, gio_hang__hoan_thanh=False, kich_thuoc=kich_thuoc)
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

# tính năng xem sản phẩm (hoặc là hiển thị trang product-detail)
def product_detail(request, san_pham_id):
    san_pham = SanPham.objects.get(pk=san_pham_id)
    theloai_list = TheLoai.objects.all()

    # Lấy ngẫu nhiên 4 sản phẩm để hiển thị ở phẩn bạn có thể quan tâm
    random_san_pham_list = SanPham.objects.order_by('?')[:4]

    context = {
        'san_pham' : san_pham, 
        'theloai_list' : theloai_list,
        'random_san_pham_list' : random_san_pham_list,
    }
    return render(request, 'app/product-detail.html', context)


    
# Hiển thị trang checkout
def checkout(request):
    theloai_list = TheLoai.objects.all()
    gio_hang = GioHang.objects.get(khach_hang=request.user, hoan_thanh=False)
    muc_gio_hang = MucGioHang.objects.filter(gio_hang=gio_hang)
    gia_tri_gio_hang = 0
    for muc in muc_gio_hang:
        muc.tong_gia_cua_tung_muc = muc.tinh_tong_gia_cua_tung_muc()
        gia_tri_gio_hang += muc.tong_gia_cua_tung_muc

    context = {
        'muc_gio_hang' : muc_gio_hang,
        'gia_tri_gio_hang' : gia_tri_gio_hang,
        'theloai_list' : theloai_list,
    }

    if request.method == "POST":
        ten_nguoi_nhan = request.POST['name']
        email = request.POST['email']
        sdt = request.POST['phone']
        dia_chi = request.POST['address']
        thanh_pho = request.POST['city']
        quan = request.POST['district']
        phuong = request.POST['ward']
        
        dia_chi_giao_hang = DiaChiGiaoHang.objects.create(
            khach_hang = request.user,
            gio_hang = gio_hang,
            sdt = sdt,
            email = email,
            dia_chi = dia_chi,
            thanh_pho = thanh_pho, 
            quan = quan,
            phuong = phuong,
            ten_nguoi_nhan = ten_nguoi_nhan
        )
        dia_chi_giao_hang.save()

        gio_hang.hoan_thanh = True
        gio_hang.save()
        messages.success(request, 'Đặt hàng thành công')
        return redirect ('home')
          
    return render(request, 'app/checkout.html', context)



# tính năng tìm kiếm sản phẩm (hiển thị trang search)
def search(request):
   
    query = request.GET.get('search', '')
    if query: 
        san_pham_tim_kiem_list = SanPham.objects.filter(ten__icontains=query)
    else: 
        san_pham_tim_kiem_list = SanPham.objects.none()
    context = {
        'query' : query,
        'san_pham_tim_kiem_list' : san_pham_tim_kiem_list,
    }
    return render(request, 'app/search.html', context)

# Hiển thị trang user profile của người dùng
def user_profile(request):
    theloai_list = TheLoai.objects.all()
    profile, created = Profile.objects.get_or_create(khach_hang=request.user)
    if request.method == 'POST':
        # Phần này là làm về cập nhật thông tin user
        hinh = request.FILES.get('hinh')
        ho_ten = request.POST.get('ho-ten')
        sdt = request.POST.get('sdt')
        ngay_sinh = request.POST.get('ngay-sinh')

        if hinh == None:
            hinh = profile.hinh

        profile.hinh = hinh 
        profile.ho_ten = ho_ten
        profile.sdt = sdt

        if ngay_sinh:
            profile.ngay_sinh = ngay_sinh
        
        profile.save()
        
        # Phần này là làm về thay đổi password 
        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        repeat_new_password = request.POST.get('repeat-new-password')
        username = request.user.username

        user = authenticate(request, username=username, password=current_password)
        if user is not None: 
            if new_password == repeat_new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Thay đổi mật khẩu thành công')
                return redirect('login_user')
            else: 
                return redirect('user_profile')
        else:
            return redirect('user_profile') 
    context = {
        'profile' : profile,
        'theloai_list' : theloai_list,
    }
    return render(request, 'app/user-profile.html', context)


# Hiển thị trang Đơn Hàng 
def donhang(request):
    theloai_list = TheLoai .objects.all()
    gio_hang_nguoi_dung = GioHang.objects.filter(khach_hang=request.user, hoan_thanh = True)
    context = {     
        'gio_hang_nguoi_dung' : gio_hang_nguoi_dung,
        'theloai_list' : theloai_list,
    }

    return render(request, 'app/donhang.html', context)

# Hiển thị trang about (Giới thiệu)
def about(request):
    return render(request, 'app/about.html')
                

