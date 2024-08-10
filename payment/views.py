from datetime import datetime, timedelta
from django.shortcuts import render
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework import status
from api.models import *
from django.conf import settings
from payment.models import Payment
from booking.models import Booking
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdmin, IsTutor
from payment.paginations import *
from payment.serializers import *
from django.db.models import Sum
from api.models import User, City, Subject
from booking.models import Booking
from rating.models import Feedback
from django_filters.rest_framework import DjangoFilterBackend
from payment.filters import  PaymentFilter

# Create your views here.

import stripe

# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


class StripeCheckoutView(APIView):
    def post(self, request):
        price = request.data.get("price")
        tutor_id = request.data.get("tutor_id")
        booking_id = request.data.get("booking_id")
        user_id = request.user.id
        try:

            # stripe accepts ind money as paise so we need to convert amount in paise
            price_in_paise = int(float(price) * 100)
            product = stripe.Product.create(name=f"Tutor Payment - {tutor_id}")

            # Create a price object in Stripe
            price_object = stripe.Price.create(
                unit_amount=price_in_paise,
                currency="inr",
                product=product.id,
            )

            intent = stripe.PaymentIntent.create(
                amount=price_in_paise,
                currency="inr",
                metadata={
                    "user_id": user_id,
                    "total_price": price_in_paise,
                    "booking_id": booking_id,
                    "tutor_id": tutor_id,
                },
            )
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": price_object.id,
                        "quantity": 1,
                    },
                ],
                payment_method_types=["card"],
                mode="payment",
                success_url="http://localhost:3000/payment/success",
                cancel_url="http://localhost:3000/payment/fails",
                metadata={
                    "user_id": user_id,
                    "total_price": price_in_paise,
                    "booking_id": booking_id,
                    "tutor_id": tutor_id,
                },
            )
            return Response({"sessionId": checkout_session.id})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class StripeWebhookView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.headers.get("Stripe-Signature")
        endpoint_secret = os.environ.get("STRIPE_ENDPOINT_SECRET")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            payment_intent = session.get("payment_intent")

            tutor_total_amount = session.get("amount_total") / 100
            admin_amount = (
                tutor_total_amount * 0.1
            )  # 10% amount will be send to admin for using his site
            tutor_amount = (
                tutor_total_amount - admin_amount
            )  # tutor payment after deduction of admin 10 %

            metadata = session.get("metadata")

            try:
                user_id = metadata.get("user_id")
                tutor_id = metadata.get("tutor_id")
                booking_id = metadata.get("booking_id")

                user = User.objects.get(pk=user_id)
                tutor = User.objects.get(pk=tutor_id)
                booking = Booking.objects.get(pk=booking_id)

                Payment.objects.create(
                    user_id=user,
                    tutor_id=tutor,
                    booking_id=booking,
                    admin_amount=admin_amount,
                    tutor_amount=tutor_amount,
                    payment_date=datetime.now(),
                    payment_intent=payment_intent,
                )

                # updating booking status so user dont have to pay again if success
                booking = Booking.objects.get(pk=booking_id)
                booking.payment_status = "Paid"
                booking.save()

            except User.DoesNotExist:
                return HttpResponse(status=400)

        return HttpResponse(status=200)


class AdminPaymentDetailsApi(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Payment.objects.all()
    pagination_class = AdminPaymentPagination
    serializer_class = AdminPaymentSerializer


class TutorPaymentDetailsApi(ListAPIView):
    permission_classes = [IsAuthenticated, IsTutor]
    pagination_class = TutorPaymentPagination
    serializer_class = TutorPaymentSerializer

    def get_queryset(self):
        # Filter payments by the tutor's user ID
        user = self.request.user
        return Payment.objects.filter(tutor_id=user.id)


class AdminTotalEarningApi(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            # calculating total admin earning
            total_earning = Payment.objects.aggregate(total=Sum("admin_amount"))
            total_earning_value = (
                total_earning["total"] if total_earning["total"] is not None else 0
            )

            # calculating last 30 days income
            thirty_days_ago = timezone.now() - timedelta(days=30)
            payments = Payment.objects.filter(
                payment_date__gte=thirty_days_ago
            ).aggregate(total=Sum("admin_amount"))
            total_earning_30_days = payments["total"]

            # total user
            total_user = User.objects.filter(role=3).filter(isDeleted=False).count()

            # total approved tutor
            totat_approved_tutor = (
                User.objects.filter(role=2).filter(tutor_approve=True).count()
            )

            # total blocked tutor
            total_blocked_tutor = (
                User.objects.filter(role=2).filter(user_blocked=True).count()
            )

            # total booking
            total_booking = Booking.objects.count()

            return Response(
                {
                    "total_earning": total_earning_value,
                    "Last_month_earning": total_earning_30_days,
                    "total_user": total_user,
                    "total_approved_tutor": totat_approved_tutor,
                    "total_blocked_tutor": total_blocked_tutor,
                    "total_booking": total_booking,
                },
                status=200,
            )
        except Exception as e:
            return Response(
                {"Error": "Something went wrong while fetching the total earnings."},
                status=500,
            )


class TutorTotalEarningApi(APIView):
    permission_classes = [IsAuthenticated, IsTutor]

    def get(self, request):
        try:
            user = request.user

            # total earning of tutor
            total_earning = Payment.objects.filter(tutor_id=user.id).aggregate(
                total=Sum("tutor_amount")
            )
            total_earning_value = (
                total_earning["total"] if total_earning["total"] is not None else 0
            )

            # tutor last 30 days earnig
            # thirty_days_ago = timezone.now() - timedelta(days=30)
            start_date = timezone.now() - timedelta(days=30)

            payments = (
                Payment.objects.filter(tutor_id=user.id)
                .filter(payment_date__gte=start_date)
                .aggregate(total=Sum("tutor_amount"))
            )
            monthly_income = payments['total'] or 0
            
            
            total_request = Booking.objects.filter(tutor_id=user.id).count() or 0
            
            pending = Booking.objects.filter(tutor_id=user.id).filter(status='Pending').count() or 0
            
            accepted = Booking.objects.filter(tutor_id=user.id).filter(status='Accepted').count() or 0
            
            rejected = Booking.objects.filter(tutor_id=user.id).filter(status='Rejected').count() or 0

            paid = Booking.objects.filter(tutor_id=user.id).filter(payment_status='Paid').count() or 0
            

            return Response({
                "total_earning": total_earning_value,
                'monthly_income':monthly_income,
                'pending_request':pending,
                'accpted_request':accepted,
                'rejected_request':rejected,
                'total_request':total_request,
                'payment_paid':paid,
                }, status=200)
        except Exception as e:
            return Response(
                {"Error": "Something went wrong while fetching the total earnings."},
                status=500,
            )
            

class PaymentDataOfTutorApi(ListAPIView):
    permission_classes = [IsAuthenticated, IsTutor]
    serializer_class = TutorPaymentSerializer
    pagination_class = PaymentPaginationLimited
    filter_backends = [DjangoFilterBackend]
    filterset_class  = PaymentFilter
    
    def get_queryset(self):
        return Payment.objects.filter(tutor_id=self.request.user.id).all()
    
class PaymentDataOfAdminApi(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminPaymentSerializer
    pagination_class = PaymentPaginationLimited
    filter_backends = [DjangoFilterBackend]
    filterset_class  = PaymentFilter
    queryset = Payment.objects.all()
    