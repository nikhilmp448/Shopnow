from django.shortcuts import render

from products.models import OrderItem

# Create your views here.
def add_coupon(request , code):
    try:
        order = OrderItem.objects.get(user=request.user)
