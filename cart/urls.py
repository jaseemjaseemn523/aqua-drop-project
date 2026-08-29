from django.urls import path
from .views import CartDetailView, AddToCartView, UpdateCartItemView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    path('item/<int:pk>/', UpdateCartItemView.as_view(), name='update_cart_item'),
]