from django.db import models

class Member(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    birthdate = models.DateField(default='2000-01-01')
    email = models.EmailField(default='')
    price = models.DecimalField(decimal_places=2, max_digits=4, default=0.00)


