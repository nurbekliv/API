from django.contrib import admin
from .models import CustomUser
from .custom_model import Category, Product, ProductImage, ShippingHistory, PriceHistory


admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ShippingHistory)
admin.site.register(PriceHistory)
