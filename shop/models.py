from django.db import models
from accounts.models import User

# Create your models here.

class Products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Product_Name = models.CharField(max_length=50)
    Description = models.CharField(max_length=120, null=True, blank=True)
    Quantity = models.IntegerField(default=1)
    Brand_Name = models.CharField(max_length=50, null=True, blank=True)
    Price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=50)
    Product_Image = models.ImageField(upload_to='product_image')

    def __str__(self):
        return f'{self.Product_Name} of {self.user.first_name}'
    
