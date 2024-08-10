from django.contrib import admin
from django.urls import path,include
from payment.views import *

urlpatterns = [
    path('create-checkout-session/', StripeCheckoutView.as_view(), name='booking-test-api-view'),
    # path('webhook/stripe/', stripe_webhook, name='booking-test-api-view'),
    path('webhook/stripe/', StripeWebhookView.as_view(), name='booking-test-api-view'),
    
    # admin payment
    path('admin/payment/', AdminPaymentDetailsApi.as_view(), name='admin-check-his-earning'),
    path('admin/total-earning/', AdminTotalEarningApi.as_view(), name='admin-check-his-earning'),
    path('admin/all-payment/', PaymentDataOfAdminApi.as_view(), name='tutor-get-all-payment'),
    
    # tutor payment
    path('tutor/payment/', TutorPaymentDetailsApi.as_view(), name='admin-check-his-earning'),
    path('tutor/total-earning/', TutorTotalEarningApi.as_view(), name='admin-check-his-earning'),
    path('tutor/all-payment/', PaymentDataOfTutorApi.as_view(), name='tutor-get-all-payment'),
]
