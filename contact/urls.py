from django.contrib import admin
from django.urls import path,include
from contact.views import ContactUsCreateView,ContactRetieveUpdateDeleteView

urlpatterns = [
    path('create-contact-us/', ContactUsCreateView.as_view(), name='contact-us-create-view'),
    path('contact-us-details/<int:pk>/', ContactRetieveUpdateDeleteView.as_view(), name='contact-us-create-view'),
]
