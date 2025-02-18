from django.db.models import CharField, DecimalField, TextField, IntegerField, DateTimeField, ManyToManyField, ForeignKey, CASCADE

class Product(Model):
    name = CharField(max_length=200)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField()
    stock = IntegerField()
    created_at = DateTimeField(auto_now_add=True)

class Order(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    products = ManyToManyField(Product, through='OrderItem')
    total_price = DecimalField(max_digits=10, decimal_places=2)
    status = CharField(max_length=50, default='pending')

class OrderItem(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    order = ForeignKey(Order, on_delete=CASCADE)
    quantity = IntegerField()
