from django.contrib import admin
from .models import Product, ProductCategory

# Register your models here.
@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'name', 'category', 'price']
    search_fields = ['name', 'category_id']
    exclude = ('deleted_at', )
    readonly_fields = ('slug', )

    def category(self, obj):
        return obj.category_id


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']
    exclude = ('deleted_at', )