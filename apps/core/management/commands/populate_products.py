from django.core.management.base import BaseCommand
from apps.product_management.models import Product, ProductCategory
from faker import Faker
import random
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populate the database with fake products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num',
            type=int,
            default=10,
            help='Number of fake products to create',
        )

    def handle(self, *args, **options):
        num_products = options['num']
        fake = Faker()

        for _ in range(num_products):
            # Generate random data for the product
            category = ProductCategory.objects.get(id=random.randint(1, 13))  # Random category ID between 1 and 13
            brand = fake.company()
            name = fake.word().capitalize()
            description = fake.text(max_nb_chars=200)
            price = round(random.uniform(10, 1000), 2)  # Price between 10 and 1000
            stock = random.randint(1, 1000)  # Random stock quantity

            # Create and save the Product object
            product = Product(
                category_id=category,
                brand=brand,
                name=name,
                description=description,
                price=price,
                stock=stock
            )
            product.slug = slugify(f"{brand}-{name}")  # Automatically generate the slug
            product.save()

            print(f"Inserted Product: {product.name} under {category.category}")

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_products} products'))
