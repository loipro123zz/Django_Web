 
from .views import lay_so_luong_san_pham_trong_gio_hang

def tong_san_pham_trong_gio_hang(request):
    return {
        'tong_san_pham_trong_gio_hang': lay_so_luong_san_pham_trong_gio_hang(request.user)
    }