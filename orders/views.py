from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'role', '') == 'ADMIN':
            return Order.objects.all().order_by('-created_at')
        elif getattr(user, 'role', '') == 'DELIVERY':
            return Order.objects.filter(delivery_person=user).order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart or not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # ഫ്രണ്ട്‌എൻഡിൽ നിന്ന് വരുന്നത് അല്ലെങ്കിൽ യൂസർ പ്രൊഫൈലിലുള്ള അഡ്രസ്സ് എടുക്കുന്നു
        shipping_address = request.data.get('shipping_address') or getattr(user, 'address', '')
        payment_method = request.data.get('payment_method', 'COD')

        if not shipping_address:
            return Response({'error': 'Shipping address is required.'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.product.price * item.quantity for item in cart.items.all())
        payment_status = Order.PaymentStatus.PAID if payment_method == 'ONLINE' else Order.PaymentStatus.PENDING

        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,  # കസ്റ്റമറുടെ ലൊക്കേഷൻ ഇവിടെ സേവ് ആകുന്നു
            total_amount=total_amount,
            payment_method=payment_method,
            payment_status=payment_status
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )

        # Clear cart after order is placed
        cart.items.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)