# Generated by Django 5.1 on 2024-09-05 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CreatedAt')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UpdatedAt')),
                ('deleted_at', models.DateTimeField(blank=True, db_column='DeletedAt', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('role', models.CharField(db_column='Role', max_length=100, unique=True)),
            ],
            options={
                'db_table': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CreatedAt')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UpdatedAt')),
                ('deleted_at', models.DateTimeField(blank=True, db_column='DeletedAt', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('endpoint', models.CharField(db_column='Endpoint', max_length=100)),
                ('method', models.CharField(db_column='Method', max_length=10)),
                ('description', models.CharField(blank=True, db_column='Description', max_length=300, null=True)),
            ],
            options={
                'db_table': 'Permissions',
                'unique_together': {('endpoint', 'method')},
            },
        ),
        migrations.CreateModel(
            name='MemberRole',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CreatedAt')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UpdatedAt')),
                ('deleted_at', models.DateTimeField(blank=True, db_column='DeletedAt', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('member', models.ForeignKey(db_column='MemberId', on_delete=django.db.models.deletion.CASCADE, to='member_management.member')),
                ('role', models.ForeignKey(db_column='RoleId', on_delete=django.db.models.deletion.CASCADE, to='authentications.role')),
            ],
            options={
                'db_table': 'MemberRoles',
                'unique_together': {('role', 'member')},
            },
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='CreatedAt')),
                ('updated_at', models.DateTimeField(auto_now=True, db_column='UpdatedAt')),
                ('deleted_at', models.DateTimeField(blank=True, db_column='DeletedAt', null=True)),
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('permission', models.ForeignKey(db_column='PermissionId', on_delete=django.db.models.deletion.CASCADE, to='authentications.permission')),
                ('role', models.ForeignKey(db_column='RoleId', on_delete=django.db.models.deletion.CASCADE, to='authentications.role')),
            ],
            options={
                'db_table': 'RolePermissions',
                'unique_together': {('role', 'permission')},
            },
        ),
    ]
