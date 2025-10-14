from django.contrib import admin
from django.urls import path,include
from .views import ProductListCreateView,CategoryListCreateView,ProductDetailAPIView,CategoryDetailAPIView,CartAPIView,CartItemCreateAPIView,CartItemUpdateView,OrderItemCreateAPI,OrderDetailAPIView,OrderListAPIView,OrderPayAPIView,OrderCancelAPIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
urlpatterns = [
    path('api/products/' ,ProductListCreateView.as_view() ,name='product-list-create'),
    path('api/products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/categories/' ,CategoryListCreateView.as_view() ,name='categories-list-create'),
    path('api/categories/<int:pk>/' ,CategoryDetailAPIView.as_view() ,name='categories-list-create'),
    path("api/cart/", CartAPIView.as_view(), name="cart-detail"),
    path("api/cart/items/", CartItemCreateAPIView.as_view(), name="cartitem-create"),
    path("api/cart/items/<int:pk>/", CartItemUpdateView.as_view(), name="cartitem-detail"),
    path("api/orders/checkout/", OrderItemCreateAPI.as_view(), name="order-checkout"),
    path("api/orders/<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("api/orders/", OrderListAPIView.as_view(), name="order-list"),
    path("api/orders/<int:pk>/pay/", OrderPayAPIView.as_view(), name="order-pay"),
    path("api/orders/<int:pk>/cancel/", OrderCancelAPIView.as_view(), name="order-cancel"),
    path('api/token/',TokenObtainPairView.as_view(),name='token-pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='refresh-token'),
    path('api/token/verify/',TokenVerifyView.as_view(),name='token-verify')


]