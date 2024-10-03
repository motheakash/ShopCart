from rest_framework import serializers
from .models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        exclude = ['deleted_at', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    category_id = ProductCategorySerializer()

    class Meta:
        model = Product
        exclude = ['deleted_at', 'created_at', 'updated_at']


class ValidateProduct(serializers.Serializer):
    name = serializers.CharField(required=True)
    brand = serializers.CharField(required=True)
    description = serializers.CharField()
    price = serializers.CharField(required=True)
    stock = serializers.IntegerField(required=True)
    category_id = serializers.IntegerField(required=True)
    
