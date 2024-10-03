from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from typing import Any, Union, List
from rest_framework.request import Request
from django.utils.decorators import method_decorator
from apps.core.utils import CustomPagination
from .service import ProductService
from .serializers import ProductSerializer, ValidateProduct
from apps.authentications.permissions import IsAuthenticated, is_authorized
from cache_layer.decorators import cache_decorator
from .models import ProductCategory, Product



class ProductAPI(APIView):
    pagination_class = CustomPagination
    service_class = ProductService
    serializer_class = ProductSerializer
    validation_class = ValidateProduct
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.service_class.get_all_products()

    @method_decorator(is_authorized)
    @method_decorator(cache_decorator(ttl=60), name='get')
    def get(self, request, *args, **kwargs):
        try:
            page_size: int = int(request.GET.get('page_size', 10))
            paginator: CustomPagination = self.pagination_class()
            paginator.page_size = page_size

            queryset = self.get_queryset()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def post(self, request, *args, **kwargs):
        try:
            payload = request.data
            validation_serializer = ValidateProduct(data=payload)
        
            if not validation_serializer.is_valid():
                raise ValidationError(validation_serializer.errors)
            
            validated_data = validation_serializer.validated_data

            try:
                validated_data['category_id'] = ProductCategory.objects.get(id=validated_data.pop('category_id'))
            except ProductCategory.DoesNotExist:
                return Response({'error': 'product category with category_id does not exists.'})
            
            product = self.service_class.create_product(validated_data)
            product_serializer = ProductSerializer(product)

            return Response({
                'message': 'Product created.',
                'product': product_serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
