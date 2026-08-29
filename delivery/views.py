from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from orders.models import Order
from orders.serializers import OrderSerializer
from .models import DeliveryLocation
from .serializers import DeliveryLocationSerializer, AssignDeliverySerializer

User = get_user_model()

class IsDeliveryPerson(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.DELIVERY

class AssignOrderView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = AssignDeliverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = get_object_or_404(Order, id=serializer.validated_data['order_id'])
        delivery_person = get_object_or_404(
            User, id=serializer.validated_data['delivery_person_id'], role=User.Role.DELIVERY
        )

        order.delivery_person = delivery_person
        order.status = Order.StatusChoices.CONFIRMED
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

class UpdateLocationView(views.APIView):
    permission_classes = [IsDeliveryPerson]

    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        if latitude is None or longitude is None:
            return Response({'error': 'Latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        location, _ = DeliveryLocation.objects.get_or_create(delivery_person=request.user)
        location.latitude = latitude
        location.longitude = longitude
        location.save()

        return Response(DeliveryLocationSerializer(location).data, status=status.HTTP_200_OK)

class DeliveryOrdersView(views.APIView):
    permission_classes = [IsDeliveryPerson]

    def get(self, request):
        orders = Order.objects.filter(delivery_person=request.user).order_by('-created_at')
        return Response(OrderSerializer(orders, many=True).data)

class UpdateOrderStatusByDeliveryView(views.APIView):
    permission_classes = [IsDeliveryPerson]

    def patch(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, delivery_person=request.user)
        new_status = request.data.get('status')

        if new_status in [Order.StatusChoices.OUT_FOR_DELIVERY, Order.StatusChoices.DELIVERED]:
            order.status = new_status
            if new_status == Order.StatusChoices.DELIVERED and order.payment_method == Order.PaymentMethod.COD:
                order.payment_status = Order.PaymentStatus.PAID
            order.save()
            return Response(OrderSerializer(order).data)

        return Response({'error': 'Invalid status transition for delivery person'}, status=status.HTTP_400_BAD_REQUEST)