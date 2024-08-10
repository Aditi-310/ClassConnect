from django.db import models

# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=12)
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=500)
    isDeleted = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name
