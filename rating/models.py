from django.db import models
from api.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Feedback(models.Model):
    tutor_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_tutor')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_user')
    review = models.CharField(max_length=200)
    star = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    isDeleted = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.review
    
    @property
    def get_user_profile(self):
        return f'{self.user_id.first_name}'
    