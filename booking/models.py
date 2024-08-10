from django.db import models
import uuid
from api.models import User,Subject

class Booking(models.Model):
    tutor_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_tutor')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_user')
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='booking_subject')
    booking_time = models.CharField(max_length=50)
    booking_date = models.CharField(max_length=12)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')
    cancellation_reason = models.TextField(blank=True)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid')
    isDeleted = models.BooleanField(default=False)
    usr_cancellation_reason = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return f'{self.id}'
