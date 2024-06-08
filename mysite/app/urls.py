from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_user, name="login_user"),
    path('logout', views.logout_user, name="logout_user"),
    path('register', views.register_user, name="register_user"),
    path('category/<str:tl>', views.category, name="category"),
    path('cart/', views.cart, name='cart'),
    path('them_vao_gio_hang/', views.them_vao_gio_hang, name='them_vao_gio_hang'),
    path('cap_nhat_muc_gio_hang/', views.cap_nhat_muc_gio_hang, name='cap_nhat_muc_gio_hang'),
    path('xoa_muc_gio_hang', views.xoa_muc_gio_hang, name='xoa_muc_gio_hang'),
    path('product_detail/<int:san_pham_id>', views.product_detail, name='product_detail'),
    path('checkout', views.checkout, name='checkout'),
    path('search', views.search, name='search'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('donhang', views.donhang, name='donhang'),
    path('about', views.about, name="about"),
]




