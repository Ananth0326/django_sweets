from django.urls import path
from . import views

urlpatterns = [
    # --- Main Pages ---
    path('', views.home, name='home'),
    path('sweets/', views.sweet_list, name='sweet_list'),
    path('sweets/<int:sweet_id>/', views.sweet_detail, name='sweet_detail'),
    
    # --- Cart & Checkout Flow ---
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'), 
    path('order_success/<int:order_id>/', views.order_success_view, name='order_success'), 

    # --- Original (non-AJAX) Add to Cart ---
    # We're keeping this, but not really using it on the detail page anymore
    path('cart/add/<int:sweet_id>/', views.add_to_cart, name='add_to_cart'), 
    
    # --- NEW AJAX API URLs ---
    # This is the line that fixes your error!
    path('api/add_to_cart/<int:sweet_id>/', views.add_to_cart_ajax, name='api_add_to_cart'),
    
    # This is for the little cart number in the navbar
    path('api/get_cart_count/', views.get_cart_count_api, name='api_get_cart_count'),
]