from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_signin,name="admin_signin"),
    path('admin_home/',views.admin_home,name="admin_home"),
    path('admin_signout/',views.admin_signout,name="admin_signout"),
    path('customer/',views.customer,name="customer"),
    path('order_details/',views.order_details,name="order_details"),
    path('searchtracking',views.searchtracking,name="searchtracking"),
    path('searchtrack',views.searchtrack,name="searchtrack"),
    path('edit_shipping/<str:tno>',views.edit_shipping,name="edit_shipping"),
    path('view_shipping/<str:tno>',views.view_shipping,name="view_shipping"),
    path('customer_pickoff/<customer_id>',views.customer_pickoff,name="customer_pickoff"),
    path('add_product/',views.add_product,name="add_product"),
    path('view_product/',views.view_product,name="view_product"),
    path('edit_product/<str:id>/', views.edit_product,name='product_edit'),
    path('delete-adminprod/<int:id>',views.delete_adminprod,name="delete-adminprod"),
    path('viewadminacc/',views.viewadminacc,name='viewadminacc'),
    path('edit_adminaddress/<str:id>',views.edit_adminaddress,name="edit_adminaddress"),
    path('add_adminaddress/',views.add_adminaddress,name="add_adminaddress"),
    
]
