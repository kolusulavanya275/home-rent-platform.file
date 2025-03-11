from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('rent', 'Rent'),
        ('buy', 'Buy'),
    ]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.CharField(max_length=50,default=0)
    property_type = models.CharField(max_length=4, choices=PROPERTY_TYPES, default='rent')
    rating = models.FloatField(default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    # image_url = models.CharField(max_length=255, default='default.jpg')
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)  # <-- make sure this exists!
    property_type = models.CharField(max_length=10, choices=[('Rent', 'Rent'), ('Buy', 'Buy')])

    def __str__(self):
        return self.name
