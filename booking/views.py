from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import ap
# All Booking serializer
from booking.serializers import (BookingSerializer,BookingStatusUpdateSerializer,BookingOrderSerializer)
from rest_framework import generics
from booking.filters import BookingFilter,TutorBookingFilter

# All api serializer 
from api.serializers import (TutorSeriliazer,UserSerializer)
from booking.models import Booking
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from api.permissions import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models import User
from booking.paginations import AdminBookingOrderPagination,UserBookingOrderPagination
from django_filters.rest_framework import DjangoFilterBackend
from api.utils import Utils
from threading import Thread


class CheckingView (APIView):
    serializer_class = BookingSerializer

    def get(self, request):
        try:
            booking = Booking.objects.all()
            serializer = self.serializer_class(booking, many=True)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return Response({'Error':'Booking does not exist'},status=status.HTTP_404_NOT_FOUND)


class BookingOrderView(APIView):
    # permission_classes=[IsAuthenticated,IsUser]
    def post(self,request,format=None):
        user = request.user.id
        tutor_id = request.data.get('tutor_id')
        try:
            
            tutor_data = User.objects.get(pk=tutor_id)
            if tutor_data.tutor_approve == False:
                return Response({'Error':'This Tutor is not approved yet'},status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'Error':'User does not exist'},status=status.HTTP_404_NOT_FOUND)
        print(f'user id {user} and tutor {tutor_id}')
        if int(user) == int(tutor_id):
            print('Condition checked')
            return Response({'Error':'You can not book your self'},status=status.HTTP_400_BAD_REQUEST)
        serializer = BookingOrderSerializer(data={ **request.data , "user_id" : user })
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'Order has been booked now waiting for the Approval'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
  
class TutorBookingOrderView(generics.ListAPIView):
    permission_classes = [IsTutor]
    serializer_class = BookingSerializer
    pagination_class = AdminBookingOrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class  = TutorBookingFilter
    
    def get_queryset(self):
        user = self.request.user
        tutor = TutorSeriliazer(user)
        tutorId = tutor.data['id']
        order_by = self.request.query_params.get('order_by', '-id')
        return Booking.objects.filter(tutor_id=tutorId).filter(status='Pending').order_by(order_by)
        
class TutorAllAcceptedBookingOrder(generics.ListAPIView):
    permission_classes = [IsTutor]
    serializer_class = BookingSerializer
    pagination_class = AdminBookingOrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class  = TutorBookingFilter
    
    def get_queryset(self):
        user = self.request.user
        tutor = TutorSeriliazer(user)
        order_by = self.request.query_params.get('order_by', '-id')
        tutorId = tutor.data['id']
        return Booking.objects.filter(tutor_id=tutorId).filter(status='Accepted').order_by(order_by)
    
# Tutor can Accept-Reject request

@api_view(['PATCH'])   
@permission_classes([IsTutor]) 
def updateBookingStatus(request,pk):
    try:
        booking = Booking.objects.get(pk=pk)
        tutor = TutorSeriliazer(request.user)
        tutorId = tutor.data['email']
        if str(booking.tutor_id) == str(tutorId):
            serializer = BookingStatusUpdateSerializer(booking,data = request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message':'Order has been approved'},status=status.HTTP_204_NO_CONTENT)
            return Response({'Error':'Status not found which you have provided'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Error':'This order is not booked for you'},status=status.HTTP_404_NOT_FOUND)
    except Booking.DoesNotExist:
        return Response({'Message':'Booking does not exist'})
    
@api_view(['PATCH'])   
@permission_classes([IsUser]) 
def cancelOrderByUser(request,pk):
    try:
        booking = Booking.objects.get(pk=pk)
        user = TutorSeriliazer(request.user)
        userId = user.data['email']
        if str(booking.user_id) == str(userId):
            serializer = BookingStatusUpdateSerializer(booking,data = request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message':'Order has been approved'},status=status.HTTP_204_NO_CONTENT)
            return Response({'Error':'Status not found which you have provided'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Error':'This order is not booked for you'},status=status.HTTP_404_NOT_FOUND)
    except Booking.DoesNotExist:
        return Response({'Message':'Booking does not exist'})
   
# Tutor can delete booking
@api_view(['DELETE'])
@permission_classes([IsTutor])
def deleteBookingByTutor(request,pk,format=None):
    try:
        booking = Booking.objects.filter(pk=pk)
        booking.delete()
        return Response({'Response':'Deleted'},status=status.HTTP_204_NO_CONTENT)
    except Booking.DoesNotExist:
        return Response({'Error':'No data found'},status=status.HTTP_404_NOT_FOUND)
    

# User check order confirm or not
class UserCheckOrderApproval(generics.ListAPIView):
    permission_classes=[IsAuthenticated,IsUser|IsTutor]
    pagination_class = UserBookingOrderPagination
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class  = BookingFilter
    
    def get_queryset(self):
        user = self.request.user
        userserializer = UserSerializer(user)
        order_by = self.request.query_params.get('order_by', '-id')
        return Booking.objects.filter(user_id = userserializer.data['id']).order_by(order_by)
        
    
class AdminOrderBookingApiView(generics.ListAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = BookingSerializer
    pagination_class = AdminBookingOrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class  = BookingFilter
    
    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', '-id')
        return Booking.objects.all().order_by(order_by)
    
# Tutor will send meeting link to user 
class SendMailForMeetingToUserApiView(APIView):
    permission_classes = [IsAuthenticated,IsTutor] 
    def post(self,request):
        try:
            user_id = request.data.get('user_id')
            user_email = User.objects.get(pk=user_id)
            meeting_link = request.data.get('meeting_link')
            
            data = {'meeting':meeting_link,'tutor':'pande.amul.dcs24@vnsgu.ac.in','user':user_email}
            thread = Thread(target=Utils.send_meeting_email_to_user,args=(data,))
            # Utils.send_meeting_email_to_user(data=data)
            thread.start()
            return Response({'Message':'Email has been sent to the user'},status=status.HTTP_200_OK)
            
        except:
            return Response({'Error':'Something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
