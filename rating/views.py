from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rating.models import Feedback
from rating.serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdmin,IsTutor

# Create your views here.

class UserFeedbackTutorApi(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = TutorFeedBackSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user.id
        serializer = self.get_serializer(data={**request.data,'user_id':user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFeedbackRetrieveApi(generics.ListAPIView):
    queryset = Feedback.objects.filter(isDeleted=False).all().order_by('-id')
    serializer_class = AdminSideFeedbackSerializer
    permission_classes = [IsAuthenticated,IsAdmin]
    

class FeedbackUpdateAndDeleteApi(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]
    
    def patch(self,request,pk):
        feedback = Feedback.objects.get(pk=pk)
        serializers = AdminSideFeedbackSerializer(feedback,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response({'error': 'Feedback not found'}, status=status.HTTP_404_NOT_FOUND)

        feedback.isDeleted = True
        feedback.save()
        return Response({'message': 'Feedback deleted successfully'}, status=status.HTTP_200_OK)
    
    
class TutorFeedbackGetApi(APIView):
    permission_classes = [IsAuthenticated,IsTutor]
    def get(self,request):
        try:
            tutor = request.user.id
            feedback = Feedback.objects.filter(tutor_id=tutor,isDeleted=False).filter(isApproved=True).all().order_by('-id')
            serializer = FeedbackForPerticularSeriliazer(feedback,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except :
            return Response({'error': 'Feedback not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class MainPageRatingToShowApi(APIView):
    def get(self,request):
        try:
            feedback = Feedback.objects.filter(isApproved=True).filter(isDeleted=False).order_by('-star')
            serializers = FeedbackSerializer(feedback,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except Feedback.DoesNotExist:
            return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
        