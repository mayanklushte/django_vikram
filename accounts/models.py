from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile_no = models.CharField(max_length=10)
    Country = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    pin_code = models.IntegerField()
    is_customer = models.BooleanField(default=False)
    is_shop = models.BooleanField(default=False)

    

