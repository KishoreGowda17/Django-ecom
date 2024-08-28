from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    signup_view,
    login_view,
    logout_view,
    home_view,
    cart_view,
    checkout_view,
    add_to_cart,
    remove_from_cart,
    search_view,
    please_login_view,
    new_orders,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", home_view, name="home"),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_view, name="cart"),
    path("checkout/", checkout_view, name="checkout"),
    path(
        "remove-from-cart/<int:cart_item_id>/",
        remove_from_cart,
        name="remove_from_cart",
    ),
    path('search/', search_view, name='search'),
    path('please-login/', please_login_view, name='please_login'),
    path('new-orders/', new_orders, name='new_orders'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
