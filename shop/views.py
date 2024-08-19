from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Cart, Order,CartItem
from django.http import JsonResponse
from django.db import models
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.decorators.http import require_POST

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home_view(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def please_login_view(request):
    return render(request, 'please_login.html')


def cart_view(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    grand_total = sum(item.quantity * item.product.price for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })
@login_required
def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        # Get the cart item and delete it
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return redirect('cart')


def checkout_view(request):
    if request.method == 'POST':
        order = Order(
            user=request.user,
            name=request.POST['name'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip_code=request.POST['zip'],
            email=request.POST['email'],
        )
        order.save()
        # Clear the user's cart
        Cart.objects.filter(user=request.user).delete()
        return render(request, 'order_confirmation.html')
    return render(request, 'checkout.html')

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += 1
            else:
                cart_item.quantity = 1
            cart_item.save()

            # Return a JSON response with the updated cart item count
            count = CartItem.objects.filter(cart=cart).aggregate(total=models.Sum('quantity'))['total'] or 0
            return JsonResponse({'status': 'success', 'cart_item_count': count})
        else:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def search_view(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query)  # Adjust this to match your search logic
    else:
        results = Product.objects.none()  # Return an empty queryset if no query

    return render(request, 'search_results.html', {'results': results})