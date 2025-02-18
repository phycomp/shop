from rest_framework.viewsets import ModelViewSet
from shop.models import Product, Order
from api.serializers import ProductSerializer, OrderSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
