
from shopapp.models import Account
from .models import Category, Myorder, OrderItem, Product, Wishlist,Order


def links(request):
    categories = Category.objects.all()
    return dict(categories=categories)

def counter(request):
    if request.user.is_authenticated:
        cart_item = OrderItem.objects.filter(user=request.user)
        count=cart_item.count()
    else:
        count = 0
    return dict(count=count)

def count(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        count_w=wishlist.count()
    else:
        count_w = 0
    return dict(count_w=count_w)

def total_product(request):
    product=Product.objects.all()
    p_count = product.count()
    return dict(p_count=p_count)

def total_order_count(request):
    
    canceled = Order.objects.filter(status = 'cancel')
    c1 = canceled.count()
    total_order = Order.objects.all()
    c2 = total_order.count()
    order_count = c2-c1
    return dict(order_count=order_count,c1=c1,c2=c2)

def total_user(request):
    user_count = Account.objects.all()
    u_count =user_count.count()
    return dict(u_count=u_count)

def total_revenue(request):

    order = Order.objects.filter(status = 'delivered')
    orderitem = Myorder.objects.filter(order = order.pric)
    print(orderitem)
    total_rev = 0
    for price in orderitem:
        total_rev += price.price
    return dict(total_rev=total_rev)





 