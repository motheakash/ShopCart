from .models import Product, ProductCategory


class ProductService:

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def create_product(data):
        return Product.objects.create(**data)