from rest_framework serializers import ModelSerializer
from shop.models import Product, Order

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status']
