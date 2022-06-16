from asyncio import current_task
from django import template
from requests import request
from products.models import Order, OrderItem
from shopapp.models import Account

register = template.Library()

@register.filter
def cart_count(user):
    if user.is_authenticated:
        query_set = Order.objects.filter(user=user,ordered=False)
        if query_set.exists():
            return query_set[0].items.count()
    return 0

