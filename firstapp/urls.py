from django.urls import path
from .views import (RegisterView, LogoutView, AllProductsView,
                    ProductFilterView, CartView, QuantityView, AddToCartView, ProductDetailView,
                    CartRemoveView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('products/', AllProductsView.as_view(), name='products'),
    path('product/filter/', ProductFilterView.as_view(), name='product_filter'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/remove/<int:product_id>/', CartRemoveView.as_view(), name='remove_cart'),
    path('cart/quantity/<int:product_id>/', QuantityView.as_view(), name='quantity'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/product/detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
