from rest_framework import viewsets, permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    # ലഭ്യമായ എല്ലാ പ്രൊഡക്റ്റുകളും ഫ്രണ്ട്‌എൻഡിലേക്ക് കിട്ടാൻ AllowAny നൽകുക
    queryset = Product.objects.filter(is_available=True).order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']