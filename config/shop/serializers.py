from rest_framework import serializers
from .models import Category,Product,Cart,CartItem,Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class CartItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CartItem
        fields = ('id','product','quantity','cart','subtotal')
        read_only_fields = ('cart',)
    def validate_quantity(self,value):
        if value<=0:
            raise serializers.ValidationError('Quantity must be at least 1.')
        return value
    def validate(self,attrs):
        product = attrs.get('product') or getattr(self.instance,'product',None)
        qnt = attrs.get('quantity') or getattr(self.instance,'quantity',None)
        if product is None or qnt is None:
            return attrs
        if qnt > product.stock:
            raise serializers.ValidationError({'quantity': f'Only {product.stock} items in stock.'})
        return attrs
    def get_subtotal(self,obj):
        return obj.quantity * obj.product.price
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True,read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cart
        fields = ('id','user','created_at','items','total')
        read_only_fields = ('user','created_at','items','total')
    def get_total(self,obj):
        qs = obj.items.select_related('product').all()
        return sum(item.quantity * item.product.price for item in qs)
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','user','status','created_at','items','total_price')
        read_only_fields = ('user','status','created_at')
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product','quantity','price','order')
        read_only_fields = ('price','order')
    def validate_quantity(self,value):
        if value<=0:
            raise serializers.ValidationError('Quantity must be at least 1.')
        return value