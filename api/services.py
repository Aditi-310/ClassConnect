# Trying to refactor some of my logic in here as service layer
# to make it more modular and reusable and make my serializer and view clean

from rest_framework import status
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
import logging

logger = logging.getLogger(__name__)

# user, tutor and admin related services
class UserService:
    
    @staticmethod
    def get_login_response(serializer_data, role):
        logger.info('User logged in %s',serializer_data )
        if role == '3':
            if serializer_data["isDeleted"]== 'True':
                return {"Error": "Invalid User"}, status.HTTP_401_UNAUTHORIZED
            else:
                response = {
                    "success": True,
                    "statuCode": status.HTTP_200_OK,
                    "access": serializer_data["access"],
                    "refresh": serializer_data["refresh"],
                    "user": {
                        "id": serializer_data["id"],
                        "email": serializer_data["email"],
                        "first_name": serializer_data["first_name"],
                        "last_name": serializer_data["last_name"],
                        "role": serializer_data["role"],
                        "address": serializer_data["address"],
                        "gender": serializer_data["gender"],
                        "profile_image": serializer_data["profile_image"],
                        "contact": serializer_data["contact"],
                        "isDeleted": serializer_data["isDeleted"]
                    },
                }
                return response, status.HTTP_200_OK
        elif role == '2':
            tutor = User.objects.get(email=serializer_data['email'])
            if serializer_data['isDeleted']=='True':
                return {"Error": "Invalid User"}, status.HTTP_401_UNAUTHORIZED
            elif tutor.tutor_approve == False:
                return {"Message": "You are not approved by admin yet"}, status.HTTP_401_UNAUTHORIZED
            elif tutor.user_blocked:
                return {"Message": "You have been blocked by Admin"}, status.HTTP_403_FORBIDDEN
            else:
                response = {
                    "success": True,
                    "statuCode": status.HTTP_200_OK,
                    "access": serializer_data["access"],
                    "refresh": serializer_data["refresh"],
                    "user": {
                        "id": serializer_data["id"],
                        "email": serializer_data["email"],
                        "first_name": serializer_data["first_name"],
                        "last_name": serializer_data["last_name"],
                        "role": serializer_data["role"],
                        "address": serializer_data["address"],
                        "gender": serializer_data["gender"],
                        "profile_image": serializer_data["profile_image"],
                        "contact": serializer_data["contact"],
                    },
                }
                return response, status.HTTP_200_OK
        elif role == '1':
            response = {
                "success": True,
                "statuCode": status.HTTP_200_OK,
                "access": serializer_data["access"],
                "refresh": serializer_data["refresh"],
                "user": {
                    "id": serializer_data["id"],
                    "email": serializer_data["email"],
                    "first_name": serializer_data["first_name"],
                    "last_name": serializer_data["last_name"],
                    "role": serializer_data["role"],
                    "address": serializer_data["address"],
                    "gender": serializer_data["gender"],
                    "profile_image": serializer_data["profile_image"],
                    "contact": serializer_data["contact"],
                },
            }
            return response, status.HTTP_200_OK
        else:
            return {"Error": "Invalid User Role"}, status.HTTP_401_UNAUTHORIZED
        
        
    @staticmethod
    def create_tutor_and_tokens(serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "contact": user.contact,
                "gender": user.gender,
                "address": user.address,
                "role": str(user.role),
                "profile_image": str(user.profile_image),
                "short_bio": user.short_bio,
                "city": user.city.city_name if user.city else None,
                "subjects": (
                    user.subjects.subject_name if user.subjects else None
                ),
                "experience": user.experience,
                "dob": user.dob,
                "price": user.price,
            },
        }
        return response_data, status.HTTP_200_OK
    
    
    
class UserSerializerService:
    
    @staticmethod
    def create_user(validated_data):
        print('kya idhar')
        email = validated_data.get("email")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        contact = validated_data.get("contact")
        gender = validated_data.get("gender")
        address = validated_data.get("address")
        profile_image = validated_data.get("profile_image")
        password = validated_data.get("password")
        password2 = validated_data.get("password2")
        
        if password != password2:
            print('kya isme aaya')
            raise serializers.ValidationError({"password2": "Password and Confirm Password do not match!"})
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            gender=gender,
            profile_image=profile_image,
            address=address,
        )
        user.set_password(password)
        user.save()
        
        return user
    
    @staticmethod
    def role_login(attrs):
        logger.info('User is logged in %s', attrs)
        email = attrs["email"]
        password = attrs["password"]
        
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials!")
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            update_last_login(None, user)
            validation = {
                "id": user.id,
                "access": access_token,
                "refresh": refresh_token,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "contact": user.contact,
                "address": user.address,
                "gender": user.gender,
                "profile_image": user.profile_image,
                "role": user.role,
                "isDeleted":user.isDeleted,
            }
            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credential from userlogin")
        
        
    