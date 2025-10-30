from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home Page
    path('sweets/', views.sweet_list, name='sweet_list'),
    path('sweets/<int:sweet_id>/', views.sweet_detail, name='sweet_detail'),
    path('sweets/<int:sweet_id>/order/', views.place_order, name='place_order'),
    path('add_to_cart/<int:sweet_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order_success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('remove_from_cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
