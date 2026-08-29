from rest_framework import serializers
from .models import DeliveryLocation
from orders.serializers import OrderSerializer

class DeliveryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocation
        fields = ['id', 'delivery_person', 'latitude', 'longitude', 'updated_at']
        read_only_fields = ['id', 'delivery_person', 'updated_at']

class AssignDeliverySerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    delivery_person_id = serializers.IntegerField()