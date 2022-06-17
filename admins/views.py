from decimal import Context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from admins.forms import AddProductForm
from shopapp.models import Account, Address
from products.models import Myorder, Order, Product
import pandas as pd
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from django.views.decorators.cache import never_cache
from shopapp.forms import AddressForm
# Create your views here.


@never_cache
def admin_signin(request):
    if request.user.is_authenticated :
        return redirect("admin_home")
        

    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = Account.objects.get(email=email , is_superadmin=True)
        except :
            messages.error(request, "admin does not exist")
            return HttpResponse("you are not authorised")

        user = auth.authenticate(email=email, password=password, is_superadmin=True)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login Successful")
            return redirect("admin_home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("admin_signin")

    else:
        return render(request, "sign-in.html")


def admin_signout(request):
    auth.logout(request)
    messages.success(request, "You are logged out ! ")
    return redirect("admin_signin")

@login_required(login_url='admin_signin')
def admin_home(request):
    return render (request,'admindash.html')


@login_required(login_url='admin_signin')
def customer(request):
    users = Account.objects.all()
    context = {"user": users}
    return render(request, "customer.html", context)


@login_required(login_url='admin_signin')
def customer_pickoff(request, customer_id):
    customer = Account.objects.get(pk=customer_id)
    if customer.is_active:
        customer.is_active = False
        
    else:
        customer.is_active = True
    customer.save()

    return redirect("customer")


@login_required(login_url='admin_signin')
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST,request.FILES)
        if form.is_valid():
            print('valid')
            form.save()
            print('data saved successfully')
            return redirect('add_product')
        else:
            print('product not added')
            messages.info(request,'product not added')
    else:
        form = AddProductForm()
    return render(request,'add_Products.html',{'form':form})


@login_required(login_url='admin_signin') 
def view_product(request):

    products = Product.objects.all()
    context = {"products": products}
    return render(request, "view_edit.html", context)


@login_required(login_url='admin_signin')
def edit_product(request, id) :
    product = Product.objects.get(id=id)
    if request.method == 'POST' :
        form = AddProductForm(request.POST, request.FILES, instance=product)   
        if form.is_valid() :
            form.save()
            return redirect('view_product')
        
    form = AddProductForm(instance=product)
    context = {'form' : form}
    return render(request, 'edit_product.html', context)

@login_required(login_url='admin_signin')
def delete_adminprod(request,id):
    
    adminprod =  Product.objects.get(id=id)
    adminprod.delete()
    return redirect('view_product')



@login_required(login_url='admin_signin')
def order_details(request):
    order= Order.objects.all()
    context = {'order':order}
    return render(request,'billing.html',context)


@login_required(login_url='admin_signin')
def searchtracking(request):
    track = Order.objects.filter().values_list('tracking_no',flat=True)
    productlist = list(track)
    return JsonResponse(productlist , safe=False)



def searchtrack(request):
    if request.method == 'POST':
        searched = request.POST.get('fetchtrack')
        if searched =="":
            return redirect('order_details')
        else:
            if Order.objects.filter(tracking_no = searched).first() is not None:
                order= Order.objects.filter(tracking_no = searched).first()
                orderitem = Myorder.objects.filter(order=order) 
                context ={'orderitem':orderitem , 'order':order}
                return render(request,"viewshipping.html",context)
            return redirect('order_details')
    return redirect('order_details')
    
def edit_shipping(request,tno):
    order = Order.objects.get(tracking_no = tno)
    
    if  order.status == 'pending':
        order.status = 'packed'
    elif order.status == 'packed':
        order.status = 'shipped'
    elif order.status == 'shipped':
        order.status = 'delivered'
        if order.status == 'delivered':
           if order.is_paid ==False:
               order.is_paid = True
    else:
        pass
   
    order.save()
    return redirect('order_details')


def view_shipping(request,tno):
    order= Order.objects.filter(tracking_no=tno).first()
    orderitem = Myorder.objects.filter(order=order)
    if order.status == 'delivered':
        messages.error(request, "product accepted")
    context ={'orderitem':orderitem , 'order':order}
    return render(request,"viewshipping.html",context)

def viewadminacc(request):
    addresses   =  Address.objects.filter(user=request.user)
    
    context={'address':addresses}
    return render(request,'rtl.html',context)

def add_adminaddress(request):
    if request.method=="POST":
        user=Account.objects.get(email=request.user)
        full_name=request.POST['full_name']
        address =request.POST['address']
        city=request.POST['city']
        pin_code=request.POST['pin_code']
        state=request.POST['state']
        country=request.POST['country']
        mobile=request.POST['mobile']
        landmark=request.POST['landmark']

        
        Address.objects.create(
            user=user,
            full_name=full_name,
            address=address,
            city=city,
            pin_code=pin_code,
            state=state,
            country=country,
            mobile=mobile,
            landmark=landmark,
            default = True,
            
            )
        return redirect('viewAccount')

def edit_adminaddress(request,id):
    address = Address.objects.get(id=id)
    if request.method == 'POST' :
        form = AddressForm(request.POST, instance=address)   
        if form.is_valid() :
            form.save()
            return redirect('viewadminacc')
        
    form = AddressForm(instance=address)
    context = {'form' : form}
    return render(request, 'edit_adminaddress.html', context)