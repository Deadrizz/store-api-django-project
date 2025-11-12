from django.shortcuts import render
from rest_framework import generics
from .models import Category,Product,Cart,CartItem,Order,OrderItem
from .serializers import ProductSerializer,CategorySerializer,CartSerializer,CartItemSerializer,OrderSerializer,OrderItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import serializers
from django.db import transaction
from .permissions import IsAdminOrReadOnly
from .exceptions import NotFoundKeyed, StockError, KeyedAPIException
# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['category','is_active']
    ordering_fields = ['price','created_at']
    search_fields = ['name']

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter,OrderingFilter]
    ordering_fields = ['name']
    search_fields = ['name']

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer


class CartAPIView(APIView):
    permission_classes  = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        cart,_ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)


class CartItemCreateAPIView(APIView):
    permission_classes  = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        cart,_ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product')
        quantity = serializer.validated_data.get('quantity')
        if not product:
            raise NotFoundKeyed("Product not found.", key="product")
        if not product.is_active:
            raise KeyedAPIException(detail="Product is inactive.", key="product")
        existing = CartItem.objects.filter(cart=cart,product=product).first()
        if existing:
            final_qnt = existing.quantity + quantity
            if final_qnt > product.stock:
                raise serializers.ValidationError({"quantity": f"Only {product.stock} items in stock."})
            existing.quantity = final_qnt
            existing.save()
            return Response(CartItemSerializer(existing).data,status=status.HTTP_200_OK)
        else:
            if quantity>product.stock:
                raise StockError(available=product.stock)
            else:
                item = serializer.save(cart=cart)
                return Response(CartItemSerializer(item).data,status=status.HTTP_201_CREATED)

class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self,request,pk,*args,**kwargs):
        item = get_object_or_404(CartItem,pk=pk,cart__user=request.user)
        if not item:
            raise NotFoundKeyed("Item not found.", key="item")
        serializer = CartItemSerializer(instance=item,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        if 'product' in serializer.validated_data and serializer.validated_data['product'] != item.product:
            raise KeyedAPIException(
                detail="Changing product is not allowed. Remove item and add another product.",
                key="product"
            )
        qty = serializer.validated_data.get('quantity',item.quantity)
        if qty == 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if not item.product.is_active:
            raise KeyedAPIException(detail="Product is inactive.", key="product")
        if qty > item.product.stock:
            raise StockError(available=item.product.stock)
        serializer.save()
        return Response(CartItemSerializer(item).data,status=status.HTTP_200_OK)

class CartItemDeleteAPI(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,pk,*args,**kwargs):
        item = get_object_or_404(CartItem,pk=pk,cart__user=request.user)
        if not item:
            raise NotFoundKeyed("Item not found.", key="item")
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderItemCreateAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        cart = Cart.objects.filter(user=request.user).first()
        if cart is None or cart.items.count() == 0:
            raise KeyedAPIException(detail="Cart is empty.", key="cart")
        with transaction.atomic():
            order = Order.objects.create(user=request.user,status=Order.Status.NEW)
            total = 0
            for item in cart.items.select_related('product').all():
                product = Product.objects.select_for_update().get(pk=item.product_id)
                if not product.is_active:
                    raise KeyedAPIException(detail="Product is inactive.", key="product")
                if item.quantity > product.stock:
                    raise KeyedAPIException(
                        detail="Not enough stock.",
                        key="quantity",
                        item_id=item.id,
                        product_id=product.id,
                        available=product.stock,
                    )
                item_sum = item.product.price * item.quantity
                total +=item_sum
                OrderItem.objects.create(order=order,product=product,quantity=item.quantity,price=product.price)
                product.stock -= item.quantity
                product.save()
            order.total_price = total
            order.save()
            cart.items.all().delete()
        return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)

class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk,*args,**kwargs):
        order = get_object_or_404(Order,pk=pk,user=request.user)
        if not order:
            raise NotFoundKeyed("Order not found.", key="order")
        serializer = OrderSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        order = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__product')
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class OrderPayAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,pk,*args,**kwargs):
        order = get_object_or_404(Order,pk=pk,user=request.user)
        if not order:
            raise NotFoundKeyed("Order not found.", key="order")
        if order.status != Order.Status.NEW:
           raise KeyedAPIException(detail="Only NEW orders can be paid.", key="status")
        order.status = Order.Status.PAID
        order.save()
        return Response(OrderSerializer(order).data,status=status.HTTP_200_OK)
class OrderCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,pk,*args,**kwargs):
        order = get_object_or_404(Order,pk=pk,user=request.user)
        if not order:
            raise NotFoundKeyed("Order not found.", key="order")
        if order.status != Order.Status.NEW:
            raise KeyedAPIException(detail="Only NEW orders can be cancelled.", key="status")
        with transaction.atomic():
            for item in order.items.select_related('product').all():
                product = Product.objects.select_for_update().get(pk=item.product_id)
                product.stock+=item.quantity
                product.save()
            order.status=Order.Status.CANCELLED
            order.save()
        return Response(OrderSerializer(order).data,status=status.HTTP_200_OK)
