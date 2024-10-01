from django.shortcuts import render, get_object_or_404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .custom_model import Category, PriceHistory, Product, ShippingHistory, ProductImage
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LogoutSerializer, AllProductSerializer
from drf_yasg import openapi
from .cart import Cart
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi.',
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Ro\'yxatdan o\'tishda xato.',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LogoutSerializer)
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllProductsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: AllProductSerializer(many=True)})
    def get(self, request):
        products = Product.objects.all()
        serializer = AllProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductFilterView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY,
                              description="Mahsulot kategoriyasi", type=openapi.TYPE_STRING)
        ],
        responses={200: AllProductSerializer(many=True)}
    )
    def get(self, request):
        category = request.GET.get('category')
        products = Product.objects.filter(category__name=category)
        serializer = AllProductSerializer(products, many=True)
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add_cart_item(request, product)
        cart_len = cart.cart_len(request)
        return Response({'message': 'Mahsulot qo\'shildi', 'cart_len': cart_len}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        product_serializer = AllProductSerializer(product)
        return Response({'product': product_serializer.data}, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart(request)
        total_price = cart.get_total_price(self.request)
        cart_len = cart.cart_len(self.request)
        keys = cart.get_product_keys(self.request)
        individual_prices = {}
        for key in keys:
            individual_prices[key] = cart.get_total(self.request, key)

        return Response({
            'total_price': total_price,
            'cart_len': cart_len,
            'individual_prices': individual_prices
        }, status=status.HTTP_200_OK)


class QuantityView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Mahsulot miqdorini yangilash ('plus' yoki 'minus')",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'action': openapi.Schema(type=openapi.TYPE_STRING, description="'plus' yoki 'minus'"),
            },
            required=['action']
        ),
        responses={
            200: 'Muvaffaqiyatli yangilandi',
            400: 'Noto\'g\'ri action'
        }
    )
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        action = request.data.get('action')

        if action == 'plus':
            cart.add_cart_item(request, product)
        elif action == 'minus':
            cart.remove_cart_item(request, product)
        else:
            return Response({'error': 'Noto\'g\'ri action, "plus" yoki "minus" yuboring'},
                            status=status.HTTP_400_BAD_REQUEST)

        total_price = cart.get_total_price(request)
        cart_len = cart.cart_len(request)
        individual_prices = {key: cart.get_total(request, key) for key in cart.get_product_keys(request)}

        return Response({
            'success': True,
            'total_price': total_price,
            'cart_len': cart_len,
            'individual_prices': individual_prices
        }, status=status.HTTP_200_OK)


class CartRemoveView(APIView):
    def post(self, request, product_id):
        cart = Cart(request)
        cart.remove_cart_item(request, product_id)

        cart_len = cart.cart_len(request)
        total_price = cart.get_total_price(self.request)

        individual_prices = {key: cart.get_total(request, key) for key in cart.get_product_keys(request)}
        return Response({
            'success': True,
            'cart_len': cart_len,
            'total_price': total_price,
            'individual_prices': individual_prices,
        }, status=status.HTTP_200_OK)
