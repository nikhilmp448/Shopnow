
from unicodedata import name
from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('add-to-cart',views.addtocart,name="add-to-cart"),
    path('update-cart',views.updatecart,name="update-cart"),
    path('delete-cart',views.deletecart,name="delete-cart"),
    path('viewcart/',views.viewcart,name="viewcart"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('addtowishlist',views.addtowishlist,name="addtowishlist"),
    path('delete-wishlist',views.deletewishlist,name="delete-wishlist"),
    path('myorder/<str:tno>',views.myorder,name="myorder"),
    path('checkout/',views.checkout,name="checkout"),
    path('placeorder',views.placeorder,name="placeorder"),
    path('cancel_shipping/<str:tno>',views.cancel_shipping,name="cancel_shipping"),
    path('login/',views.loginpage,name="login"),
    path('register/',views.register,name="register"),
    path('logout/',views.logoutuser,name='logout'),
    path('otp/', views.otp,name='otp'),
    path('change-password/', views.change_password, name='change-password'),
    path('store/',views.store,name='store'),
    path('store/category/<slug:category_slug>/', views.store, name='product_category'),
    path('viewAccount/',views.viewAccount,name="viewAccount"),
    path('add_address/',views.add_address,name="add_address"),
    path('edit_address/<str:id>',views.edit_address,name="edit_address"),
    path('product-details/<str:slug>/',views.product_details,name="product-details"),
    path('review',views.review,name="review"),
    path('shop/search/', views.search, name='search'),
    path('add_coupon/',views.add_coupon,name='add_coupon'),
    path('proceed_to_pay',views.razorpay,name="razorpay"),
    path('orderdisplay',views.orderdisplay,name="orderdisplay"),
    # path('payment-status',views.PaymentStatus,name='payment-status'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

