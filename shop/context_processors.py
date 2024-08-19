# shop/context_processors.py

from .models import Cart, CartItem
from django.db import models

def cart_item_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = CartItem.objects.filter(cart=cart).aggregate(total=models.Sum('quantity'))['total'] or 0
        except Cart.DoesNotExist:
            pass
    return {'cart_item_count': count}
