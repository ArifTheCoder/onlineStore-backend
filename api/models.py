from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="product_images", null=True, blank=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    count_in_stock = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

