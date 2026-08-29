from django.urls import path
from .views import AssignOrderView, UpdateLocationView, DeliveryOrdersView, UpdateOrderStatusByDeliveryView

urlpatterns = [
    path('assign/', AssignOrderView.as_view(), name='assign_order'),
    path('location/', UpdateLocationView.as_view(), name='update_location'),
    path('my-orders/', DeliveryOrdersView.as_view(), name='delivery_orders'),
    path('orders/<int:order_id>/status/', UpdateOrderStatusByDeliveryView.as_view(), name='delivery_order_status'),
]