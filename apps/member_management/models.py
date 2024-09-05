from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from apps.core.models import SoftDeleteManager, BaseModel
from .utils import encrypt_password

# Create your models here.
class Member(BaseModel):
    member_id = models.AutoField(db_column='MemberId', primary_key=True)
    username = models.CharField(db_column='Username', max_length=100, unique=True)
    first_name = models.CharField(db_column='FirstName', max_length=50)
    last_name = models.CharField(db_column='LastName', max_length=50)
    email = models.EmailField(db_column='Email', unique=True)
    phone = models.CharField(db_column='Phone', max_length=10, blank=True, null=True)
    password = models.CharField(db_column='Password', max_length=300, blank=False, null=False)
    active = models.BooleanField(db_column='Active', default=False)

    objects = SoftDeleteManager()

    class Meta:
        db_table = 'Members' 
    
    def __str__(self):
        return f'{self.member_id} {self.username}'
    

@receiver(pre_save, sender=Member)
def encrypt_password_signal(sender, instance, **kwargs):
    """
    Signal receiver to encrypt customer password before saving.
    """
    if instance.password and not instance.password.startswith('$2b'):
        instance.password = encrypt_password(instance.password)