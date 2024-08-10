from rest_framework.test import APIClient,APITestCase
from api.models import User,City,Subject
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from rest_framework import status
