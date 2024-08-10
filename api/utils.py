from django.core.mail import EmailMessage
import os
import threading
import logging

logger = logging.getLogger(__name__)

class Utils:

    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject = data['subject'],
            body = data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            # from_email='pande.amul.dcs24@vnsgu.ac.in',
            to=[data['to_email']]
        )
        email.send()
        
    @staticmethod
    def send_approve_email(data):
        email=EmailMessage(
            subject='Approval of Request',
            body='Your request has been approved, Thany you for joining us',
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data]
        )
        email.send()
        
    @staticmethod
    def send_blocked_email(data):
        email=EmailMessage(
            subject='Reject Request',
            body='You have been blocked by us so from now on you wont be able to get new request. You can contact us if thats a mistake.',
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data]
        )
        email.send()
        
    @staticmethod
    def send_meeting_email_to_user(data):
        email = EmailMessage(
            subject='Class Meeting Link',
            body=data['meeting'],
            from_email=data['tutor'],
            to=[data['user']]
        )
        email.send()
        
    # If want to sende EmailMessage instace directly from view and not create here as static method 
    # than you can use it directly and send EmailMessage insatce 
    @staticmethod
    def send_email_thread(email_instance : EmailMessage):
        email_instance.send()
        
    @staticmethod 
    def send_automate_email():
        logger.info('Working now')
        pass