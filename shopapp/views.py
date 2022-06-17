from django.views.decorators.csrf import csrf_exempt
import random
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,AddressForm
from .models import Account,Address
from django.contrib import messages , auth
from django.contrib.auth import authenticate, logout
from shopapp.otp import *
from products.models import Myorder, Order, OrderItem, Product ,Category, Wishlist
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.
def home(request):
    products = Product.objects.all()
    catogory = Category.objects.all()
    context = {'products':products , 'catogory':catogory}
    return render(request,'index.html',context)


def store(request, category_slug=None) :
    categories = None
    products = None
    
    if category_slug is not None :
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else :
        products = Product.objects.all().filter(available=True).order_by('id')
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
        
    context = {
        
        # for paginations, instead of passing the whole products, only pass paged products which will be 6 in this case.
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request, 'index2.html', context)
        
@login_required(login_url='login')
def viewAccount(request):
    addresses   =   Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    context={'addresses':addresses,'orders':orders}
    return render(request,'view_Account.html',context)

def myorder(request,tno):
    order= Order.objects.filter(user=request.user,tracking_no=tno).first()
    orderitem = Myorder.objects.filter(order=order)
    context ={'orderitem':orderitem , 'order':order}
    return render(request,"viewmyorder.html",context)    


def add_address(request):
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

def edit_address(request,id):
    address = Address.objects.get(id=id)
    if request.method == 'POST' :
        form = AddressForm(request.POST, instance=address)   
        if form.is_valid() :
            form.save()
            return redirect('viewAccount')
        
    form = AddressForm(instance=address)
    context = {'form' : form}
    return render(request, 'edit_address.html', context)

def product_details(request,slug ):
    item =Product.objects.get(slug=slug)
    context= {'item':item}
    return render(request,'product-detail.html',context)

def search(request) :
    
    if 'keyword' in request.GET :
        keyword = request.GET['keyword']
        if keyword :
            products = Product.objects.filter(Q(description__icontains = keyword) | Q(name__icontains = keyword))
            
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        else :
            products = Product.objects.all().filter(available=True).order_by('id')
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
    
    context = {
        'products' : paged_products,
        'product_count' : product_count
    }
    return render(request, 'index2.html', context)



@login_required(login_url='login')
def wishlist(request):
    wishlists  = Wishlist.objects.filter(user=request.user)
    context ={'wishlists':wishlists}
    return render(request,'wishlist.html',context)

def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Wishlist.objects.filter(user=request.user , product_id = prod_id):
                    return JsonResponse({'status':"product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user , product_id = prod_id)
                    return JsonResponse({'status':"product added to wishlist"})
            else:
                return JsonResponse({'status':"no such product found"})
        else:

            return JsonResponse({'status': "login to continue"})
    return redirect('home')

def deletewishlist(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if Wishlist.objects.filter(user=request.user,product_id=prod_id):
            wishlist_item =  Wishlist.objects.get (  product_id=prod_id , user=request.user )
            wishlist_item.delete()
        return JsonResponse({'status':"item removed"})
    return redirect('home')

@login_required(login_url='login')
def viewcart(request):
        cart =OrderItem.objects.filter(user = request.user)
        total=0
    
        for item in cart:

            if item.product.available:
                total += item.quantity * item.product.price

        context ={'cart':cart,'total':total }
        return render(request,"shoping-cart.html",context)
   
def addtocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if OrderItem.objects.filter(user=request.user.id,product_id=prod_id):
                    return JsonResponse({'status':"Product Already in cart"})
                else:
                    prod_qty = int(request.POST.get('quantity'))
                    if product_check.stock >=prod_qty:
                        OrderItem.objects.create(user=request.user, product_id=prod_id , quantity=prod_qty)
                        return JsonResponse({'status':"Product added successfully"})
                    else:
                        return JsonResponse({'status':"Only" + str(product_check.stock)+ "stock available"})
            else:
                return JsonResponse({'status':"no such product found"})
        else:
            return JsonResponse({'status':"login required"})
        
    return redirect('home')

def updatecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        product_check = Product.objects.get(id=prod_id)
        if OrderItem.objects.filter(user=request.user,product_id=prod_id):
            prod_qty = int(request.POST.get('quantity'))
            if product_check.stock >=prod_qty:
                cart = OrderItem.objects.get(  product_id=prod_id ,user=request.user)
                cart.quantity=prod_qty
                cart.save()
                return JsonResponse({'status':"updated"})
            else:
                return JsonResponse({'status':"Only" + str(product_check.stock)+ "stock available"})
        
    return redirect('home')

def deletecart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if OrderItem.objects.filter(user=request.user,product_id=prod_id):
            cart_item =  OrderItem.objects.get (  product_id=prod_id , user=request.user )
            cart_item.delete()
        return JsonResponse({'status':"item removed"})
    return redirect('home')

@login_required(login_url='login')
def checkout(request): 
    rawcart = OrderItem.objects.filter(user=request.user )
    for item in rawcart:
        if item.product.available ==False:
            OrderItem.objects.delete(id=item.id)
    cartitem = OrderItem.objects.filter(user=request.user)
    total_price = 0
    for item in cartitem:
        total_price += item.quantity * item.product.price
    return render(request,'checkout.html',{'cartitem':cartitem,'total':total_price})





@csrf_exempt
@login_required(login_url='login')
def placeorder(request):
    if request.method == "POST":
        new_order = Order()
        new_order.user = request.user
        new_order.full_name = request.POST['full_name']
        new_order.address = request.POST['address']
        new_order.city = request.POST['city']
        new_order.pin_code = request.POST['pin_code']
        new_order.state = request.POST['state']
        new_order.country = request.POST['country']
        new_order.mobile = request.POST['mobile']
        new_order.landmark = request.POST['landmark']
        new_order.payment_mode = request.POST['payment_mode']
        
    


        cart = OrderItem.objects.filter(user=request.user)
        cart_total = 0
        for item in cart:
            cart_total += item.quantity * item.product.price

        new_order.total_price = cart_total
        trackno = 'SNW'+str(random.randint(111111111,999999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'SNW'+str(random.randint(111111111,999999999))
        
        new_order.tracking_no = trackno

        if request.POST['payment_mode'] == 'COD':
            oder_id = 'COD'+str(random.randint(111111111,999999999))
            while Order.objects.filter(payment_id=oder_id) is None:
                oder_id = 'COD'+str(random.randint(111111111,999999999))
            new_order.payment_id = oder_id
        else:
            new_order.payment_id = request.POST['payment_id']
            new_order.is_paid = True

        new_order.save()

        myorder_item =OrderItem.objects.filter(user=request.user)
        for item in myorder_item:
            Myorder.objects.create(
                order = new_order,
                product = item.product,
                price = item.product.price,
                quantity = item.quantity
            )
             # to decrement the product's stock from available stock

            orderproduct = Product.objects.filter(id = item.product_id).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            if orderproduct.stock <=0:
                orderproduct.available = False
            orderproduct.save()

        # clear user cart
        OrderItem.objects.filter(user=request.user).delete()
        
        paymode = request.POST['payment_mode']
        if (paymode == 'Razorpay' or paymode == 'PayPal' ):
            # new_order.payment_id = request.POST['payment_id']
            # new_order.save()
            return JsonResponse({'status': "Your order has been placed successfully" })


    return redirect('home')


@csrf_exempt
def razorpay(request):
    cart = OrderItem.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.product.price * item.quantity
    
    return JsonResponse({
        'total_price':total_price
    })

def orderdisplay(request):
    return render(request,'status.html')

def cancel_shipping(request,tno):
    order = Order.objects.get(tracking_no = tno)
    order.status = 'cancel'
    order.save()
    stock = Myorder.objects.filter(order=order)
    for item in stock:
        product_stock = Product.objects.filter(id = item.product_id).first()
        product_stock.stock = product_stock.stock + item.quantity
        product_stock.available=True
        product_stock.save()
    return redirect('viewAccount')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email)
        except :
            messages.error(request,"user Does not exist..")
        if user.is_active:
            user = authenticate(request,email=email,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
            else:
                messages.error(request,'user does not exist..')
        else:
            messages.error(request,'You have been blocked by admin')
            return redirect('login')

    return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect('home')

def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email      = form.cleaned_data['email']
            gender     = form.cleaned_data['gender']
            mobile     = form.cleaned_data['mobile']
            password   = form.cleaned_data['password']

            request.session['first_name'] = first_name
            request.session['last_name']  = last_name
            request.session['email']      = email
            request.session['gender']     = gender
            request.session['mobile']     = mobile
            request.session['password']   = password

            sendOTP(mobile)
            return redirect('otp')

    context = {'form' : form}
    return render(request,'register.html',context)

def otp(request):
    if  request.method == 'POST':
        otp_check = request.POST.get('OTP')
        mobile=request.session['mobile']

        verify=verifyOTP(mobile,otp_check)

        if  verify:
            messages.success(request,'account has created successfuly please login now') 

            first_name = request.session['first_name']
            last_name  = request.session['last_name']
            email      = request.session['email']
            gender     = request.session['gender']
            mobile     = request.session['mobile']
            password   = request.session['password']

            user = Account.objects.create_user(
                first_name =  first_name,
                last_name  =  last_name,
                email      =  email,
                gender     =  gender,
                mobile     =  mobile,
                password   =  password
            )
            user.is_verified = True
            user.save()
            return redirect('login')
        
        else:
            messages.error(request,'invalid otp recheck')
            return redirect ('otp')
        
    return render(request,'otpverification.html')



