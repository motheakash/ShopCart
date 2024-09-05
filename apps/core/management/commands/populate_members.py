from django.core.management.base import BaseCommand
from apps.member_management.models import Member
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the database with fake members'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num',
            type=int,
            default=10,
            help='Number of fake members to create',
        )

    def handle(self, *args, **options):
        num_members = options['num']
        fake = Faker()

        phone_length = 10
        phone_number = fake.numerify(text='0' * phone_length)  # Generate random digits with specified length
        # Create a new Customer object with fake data
        for _ in range(num_members):
            customer = Member(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=phone_number,
                password=fake.password(),  # Hash the fake password
                active=fake.boolean(chance_of_getting_true=50)  # Random active status
            )
            customer.save()
            print("Data inserted")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_members} members'))
