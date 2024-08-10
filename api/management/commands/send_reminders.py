from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from booking.models import Booking
import logging
import os


logger = logging.getLogger('api') # setting logger for api app only

class Command(BaseCommand):
    help = 'Send reminder emails to tutors about their appointments'

    def handle(self, *args, **kwargs):
        try:
            today = timezone.now().date()
            bookings = Booking.objects.filter(booking_date=today).filter(status='Accepted').filter(payment_status='Paid')
            
            # 
            # email for same tutor email will stored and than it will be sent once all booking data are there 
            # for same user
            # 
            appointments_by_tutor = {} 
            

            for booking in bookings:
                tutor_email = booking.tutor_id.email
                if tutor_email not in appointments_by_tutor:
                    appointments_by_tutor[tutor_email] = []
                appointments_by_tutor[tutor_email].append(booking)
                
            for tutor_email,appointments in appointments_by_tutor.items():
                subject = "Appointment Reminder"
                message = f'Dear {appointments[0].tutor_id.first_name},\n\n'
                message += 'You have the following appointments scheduled for today:\n\n'
                for appointment in appointments:
                    message += f'Appointment with {appointment.user_id.get_full_name} on {appointment.booking_date} at {appointment.booking_time}\n'
                send_mail(subject, message, os.environ.get('EMAIL_USER'),[os.environ.get('EMAIL_USER')])

            logger.info("Daily Reminder emails sent successfully to Tutor")
        except Exception as e:
            logger.error(f"Error sending reminder emails: {e}")