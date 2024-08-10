from django.shortcuts import render
from api.serializers import (
    UserRegisterSerializer,
    UserLoginSeriliazer,
    UserSerializer,
    UserChangePasswordSerializer,
    UserPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
    TutorRegistrationSerializer,
    TutorLoginSerializer,
    TutorSeriliazer,
    TutorApproveByAdminSerializer,
    TutorApprovedSerializer,
    TutorUserBlockedByAdminSerializer,
    UserDeleteByAdminSerializer,
)
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from api.permissions import IsTutor, IsUser,IsAdmin
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from api.paginations import UserPagination,TutorPagination
# from rest_framework.filters import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TurorFilter
from api.utils import Utils
from django.db.models import Q
from rest_framework import serializers 
# from rest_framework import DjangoFilterBackend

from api.models import User
import os
from threading import Thread
from api.services import UserService

#cutom permission mixin for isAuthenticated and user permission
class IsAdminPermissionMixin:
    permission_classes = [IsAuthenticated,IsAdmin]
    
    
class IsTutorPermissionMixin:
    permission_classes=[IsAuthenticated,IsTutor]

# User registration api view
class UserRegisterApiView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # print('user save hua',user)
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                response_data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "contact": user.contact,
                        "role": str(user.role),
                        "profile_image": str(user.profile_image),
                        "gender": user.gender,
                        "address": user.address,
                    },
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            return Response(
                {"Message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# user login api view
class UserLoginApiView(APIView):
    serializer_class = UserLoginSeriliazer

    def post(self, request, format=None):
        try:

            serializer = self.serializer_class(data=request.data)

            valid = serializer.is_valid(raise_exception=False)
            status_code = status.HTTP_401_UNAUTHORIZED
            response = {
                "success": False,
                "statusCode": status_code,
                "errors": "Invalid Credentials",
            }
            if valid:
                role = serializer.data['role']
                response,status_code = UserService.get_login_response(serializer_data=serializer.data,role=role)
                return Response(response, status=status_code)
            return Response(response, status=status_code)
        except Exception as e:
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserPasswordChangeView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            return Response(
                {"Message": "Password Changed"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetEmailView(APIView):
    # permission_classes=[IsAuthenticated,IsUser]
    def post(self, request, format=None):
        serializer = UserPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"Message": "Reset password email has been sent to you"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    # permission_classes=[IsAuthenticated,IsUser]
    def post(self, request, uid, token, format=None):
        serializers = UserPasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializers.is_valid():
            return Response(
                {"Message": "Password reset successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAndUpdateApiView(APIView):
    # permission_classes = [IsUser]

    def get(self, request):
        status_code = status.HTTP_401_UNAUTHORIZED
        response = {
            "success": False,
            "statusCode": status_code,
            "errors": "Authentication credentials were not provided.",
        }
        try:
            serializer = UserSerializer(request.user)
            status_code = status.HTTP_200_OK
            response = {
                "success": True,
                "statusCode": status_code,
                "user": serializer.data,
            }
            return Response(response, status=status_code)
        except:
            return Response(response, status=status_code)

    def patch(self, request, format=None):
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {"error": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )


class TutorRegisterApiView(APIView):
    serializer_class = TutorRegistrationSerializer

    def post(self, request, format=None):
        try:
            serilaizer = self.serializer_class(data=request.data)
            if serilaizer.is_valid():
                response_data, status_code = UserService.create_tutor_and_tokens(serilaizer)
                return Response(response_data, status=status_code)
            else:
                return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {"response": "something went wrong not able to register"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TutotLoginApiView(APIView):
    serializer_class = TutorLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=False)
        status_code = status.HTTP_401_UNAUTHORIZED
        response = {
            "success": False,
            "statusCode": status_code,
            "errors": "Invalid credentials",
        }
        if valid:
            if serializer.data["role"] == "2":
                tutor = User.objects.get(email=serializer.data['email'])
                if tutor.tutor_approve == False:
                    return Response({'Message':'You are not approved by admin yet'},status=status.HTTP_401_UNAUTHORIZED)
                
                if tutor.user_blocked:
                    return Response({'Message':'You have been blocked by Admin'},status=status.HTTP_403_FORBIDDEN)
                
                status_code = status.HTTP_200_OK
                response = {
                    "success": True,
                    "statucCode": status_code,
                    "access": serializer.data["access"],
                    "refresh": serializer.data["refresh"],
                    "user": {
                        "id": serializer.data["id"],
                        "email": serializer.data["email"],
                        "first_name": serializer.data["first_name"],
                        "last_name": serializer.data["last_name"],
                        "contact": serializer.data["contact"],
                        "gender": serializer.data["gender"],
                        "address": serializer.data["address"],
                        "profile_image": serializer.data["profile_image"],
                        "dob": serializer.data["dob"],
                        "price": serializer.data["price"],
                        "short_bio": serializer.data["short_bio"],
                        "city": serializer.data["city"],
                        "subjects": serializer.data["subjects"],
                        "role": serializer.data["role"],
                        "tutor_approve":serializer.data["tutor_approve"]
                    },
                }
            return Response(response, status=status_code)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class TutorProfifeAndUpdateApiView(APIView):
    serializer_class = TutorSeriliazer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_code = status.HTTP_401_UNAUTHORIZED
        response = {
            "success": False,
            "statusCode": status_code,
            "errors": "Authentication credentials were not provided.",
        }
        try:
            status_code = status.HTTP_200_OK
            serializer = self.serializer_class(request.user)
            response = {
                "success": True,
                "statusCode": status_code,
                "user": serializer.data,
            }
            return Response(response, status=status_code)
        except:
            return Response(response, status=status_code)

    def patch(self, request, format=None):
        user = request.user
        seriliazer = self.serializer_class(user, request.data, partial=True)

        if seriliazer.is_valid():
            seriliazer.save()
            return Response(seriliazer.data, status=status.HTTP_200_OK)
        return Response(seriliazer.errors, status=status.HTTP_401_UNAUTHORIZED)


class AdminLoginView(APIView):
    serializer_class = UserLoginSeriliazer
    
    def post(self,request,format=None):
        serializer = UserLoginSeriliazer(data=request.data)
        valid = serializer.is_valid(raise_exception=False)
        status_code = status.HTTP_401_UNAUTHORIZED
        response = {
            'success':False,
            'statusCode':status_code,
            'errors':'Invalid credentials'
        }
        if valid:
            if serializer.data["role"]=='1':
                status_code = status.HTTP_200_OK
                response = {
                    'success':True,
                    'statusCode':status_code,
                    'access':serializer.data['access'],
                    'refresh':serializer.data['refresh'],
                    'user':{
                        'id':serializer.data['id'],
                        'eamil':serializer.data['email'],
                        'role':serializer.data['role']
                    }
                }
        return Response(response,status=status_code)


class AdminTutorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get("search", "")
        user = User.tutorObject.get_all_tutor(search)
        if not user:
            return Response(
                {"Error": "No Tutor found in database"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = TutorSeriliazer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            if user.role == 3 or user.role == 1:
                return Response({"Message": "This user is not Tutor"})
            if user.tutor_approve == True:
                return Response(
                    {"Message", "You first have to disable this tutor than delete"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            user.delete()
            return Response({"Message": "Deleted"})
        except:
            return Response({"Error": "Tutor not found"})
    
class AdminAllApprovedTutorView(generics.ListAPIView):
    queryset = User.tutorObject.get_approve_tutor()
    serializer_class = TutorApprovedSerializer
    pagination_class = TutorPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class  = TurorFilter
    def get_queryset(self):
        # Get the 'order_by' parameter from the query parameters
        order_by = self.request.query_params.get('order_by', '-id')
        # Pass the 'order_by' parameter to the manager method
        return User.tutorObject.get_approve_tutor(order_by=order_by)

       
class  AdminBlockedTutorOrUserView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = TutorUserBlockedByAdminSerializer
    def patch(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'Message':'User does not exist'},status=status.HTTP_404_NOT_FOUND)
        if not user:
            return Response({'Error':'User not found for this id'},status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user,data=request.data,partial=True)
        
        
        if serializer.is_valid():
            data = user.email
            serializer.save()
            approved = serializer.data['user_blocked']
            if approved == True:
                thread = Thread(target=Utils.send_blocked_email,args=(data,))
                thread.start()
                # Utils.send_blocked_email(data)
            else:
                thread = Thread(target=Utils.send_approve_email,args=(data,))
                # Utils.send_approve_email(data)
                thread.start()
            return Response({'message':'Updated user status'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class getBlockedTutorApiView(generics.ListAPIView):
    serializer_class = TutorSeriliazer
    pagination_class = TutorPagination
    queryset = User.tutorObject.get_all_blocked_tutor()

    def get_queryset(self):
        queryset = User.tutorObject.get_all_blocked_tutor()
        query = self.request.query_params.get('search')
        if query:
            queryset = queryset.filter(first_name__icontains=query)
        return queryset
@api_view(['GET']) 
@permission_classes([IsAdmin])
def getBlockedUserTutorApiView(request):
    try:
        user = User.tutorObject.get_all_blocked_tutor()
        serializer = TutorSeriliazer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'Message':'User does not exist'},status=status.HTTP_404_NOT_FOUND)
     
class AdminNotApprovedTutorView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        user = User.tutorObject.get_not_approve_tutor()
        if not user:
            return Response({'Message':'All tutor are approved right now'},status=status.HTTP_200_OK)
        serializer = TutorSeriliazer(user,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdminNotApprovedTutorApiView(generics.ListAPIView):
    queryset = User.tutorObject.get_not_approve_tutor()
    serializer_class = TutorSeriliazer
    permission_classes = [IsAdminUser]
    pagination_class = UserPagination
    
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def approveTutorByAdmin(request,pk):
    if request.method == 'PATCH':
        try:    
            user  = User.tutorObject.get_tutor_by_id(pk)
        except User.DoesNotExist:
            return Response({'Message':'User does not exist'},status=status.HTTP_404_NOT_FOUND)
        if not user:
            return Response({'Error':'User not found  for this id'},status=status.HTTP_404_NOT_FOUND)
        serializers = TutorApproveByAdminSerializer(user,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            Utils.send_approve_email(user.email)
            return Response({'Message':'Tutor Updated'})
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'Error':'Wrong Method'})
    
class AdminAllUserDataApiView(generics.ListAPIView):
    # def get
    # pagination_class
    queryset = User.userObject.get_all_user()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = UserPagination
    
    def get_queryset(self):
        # queryset = User.userObject.get_all_user()
        query = self.request.query_params.get('search')
        if query:
            queryset = User.userObject.get_all_user().filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query) | Q(address__icontains=query) 
                # Add more fields to search here
            )
        else:
            queryset = self.queryset
        return queryset
    
class TutorDataByIdApiView(APIView):
    serializer_class = TutorSeriliazer
    def get(self,request,pk):
        try:
            user = User.tutorObject.get_tutor_by_id(pk)
        except User.DoesNotExist:
            return Response({'Message':'User does not exist'},status=status.HTTP_404_NOT_FOUND)
        if not user:
            return Response({'Error':'User not found  for this id'},status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class DeleteUserOrTutorApi(IsAdminPermissionMixin,APIView):
    # permission_classes = [IsAuthenticated,IsAdmin]
    serializer_class = UserDeleteByAdminSerializer
    def patch(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = self.serializer_class(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message':'User has been deleted'},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'Error':'User does not exist'},status=status.HTTP_404_NOT_FOUND)
