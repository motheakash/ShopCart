# Generated by Django 5.1 on 2024-09-05 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CreatedAt')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UpdatedAt')),
                ('deleted_at', models.DateTimeField(blank=True, db_column='DeletedAt', null=True)),
                ('member_id', models.AutoField(db_column='MemberId', primary_key=True, serialize=False)),
                ('username', models.CharField(db_column='Username', max_length=100, unique=True)),
                ('first_name', models.CharField(db_column='FirstName', max_length=50)),
                ('last_name', models.CharField(db_column='LastName', max_length=50)),
                ('email', models.EmailField(db_column='Email', max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=10, null=True)),
                ('password', models.CharField(db_column='Password', max_length=300)),
                ('active', models.BooleanField(db_column='Active', default=False)),
            ],
            options={
                'db_table': 'Members',
            },
        ),
    ]
