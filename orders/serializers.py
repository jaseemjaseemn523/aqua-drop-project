from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.EmailField(source='user.email', read_only=True)
    customer_phone = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'customer_email', 'customer_phone', 'delivery_person', 
            'shipping_address', 'total_amount', 'status', 'payment_method', 
            'payment_status', 'items', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'delivery_person', 'status', 'payment_status', 'created_at']