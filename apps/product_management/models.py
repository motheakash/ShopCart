from django.db import models
from apps.core.models import BaseModel, SoftDeleteManager
from django.utils.text import slugify

# Create your models here.
class ProductCategory(BaseModel):
    id = models.AutoField(db_column="Id", primary_key=True)
    category = models.CharField(db_column="Category", max_length=50)

    def __str__(self) -> str:
        return f"{self.category}"

    class Meta:
        db_table = "ProductCategory"


class Product(BaseModel):
    product_id = models.AutoField(db_column="ProductId", primary_key=True)
    category_id = models.ForeignKey(ProductCategory, db_column='CategoryId', on_delete=models.CASCADE)
    brand = models.CharField(db_column="Brand", max_length=100)
    name = models.CharField(db_column="Name", max_length=100)
    description = models.TextField(db_column="Description", blank=True, null=True)
    price = models.FloatField(db_column="Price")
    stock = models.PositiveIntegerField(db_column="Stock")
    slug = models.SlugField(db_column="Slug", unique=True, blank=True)

    objects = SoftDeleteManager()

    def __str__(self) -> str:
        return f"{self.product_id}-{self.name}"

    class Meta:
        db_table = "Products"