from django.contrib import admin 
from django.urls import path,include
from api.views import (AdminAllUserDataApiView, AdminNotApprovedTutorApiView, TutorDataByIdApiView, UserRegisterApiView,UserLoginApiView,UserProfileAndUpdateApiView,
                       UserPasswordChangeView,UserPasswordResetEmailView,UserPasswordResetView,
                    TutorRegisterApiView,TutotLoginApiView,TutorProfifeAndUpdateApiView,AdminAllApprovedTutorView,
                    AdminTutorView,AdminNotApprovedTutorView,approveTutorByAdmin,AdminLoginView,AdminBlockedTutorOrUserView, getBlockedTutorApiView,getBlockedUserTutorApiView,
                    DeleteUserOrTutorApi
                    )

from rest_framework_simplejwt.views import (TokenVerifyView,TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    
    # path('api/', include('api.urls')),
    path('user/login/token/verify/',TokenVerifyView.as_view(),name='user-register-api-view'),
    path('user/login/token/refresh/',TokenRefreshView.as_view(),name='user-register-api-view'),
    path('user/register/',UserRegisterApiView.as_view(),name='user-register-api-view'),
    path('user/login/',UserLoginApiView.as_view(),name='user-login-api-view'),
    path('user/profile/',UserProfileAndUpdateApiView.as_view(),name='user-profile-api-view'),
    path('user/update/',UserProfileAndUpdateApiView.as_view(),name='user-update-api-view'),
    path('user/change-password/',UserPasswordChangeView.as_view(),name='user-change-password-api-view'),
    path('user/reset-password/',UserPasswordResetEmailView.as_view(),name='user-reset-password-api-view'),
    path('user/reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='user-reset-password-uid-token-api-view'),
    
    #City api 
    path('admin/',include('cityandsubject.urls'),name='user-update-api-view'),
    
    
    #Booking Api
    path('booking/',include('booking.urls'),name='user-update-api-view'),
    
    #feedback-review api
    path('rating/',include('rating.urls'),name='user-update-api-view'),
    
    #payment
    path('payment/',include('payment.urls'),name='payment-stripe-api-view'),
    
    #contact us
    path('contact/',include('contact.urls'),name='contact-api-view'),
     
    #admin tutor
    path('admin/login/',AdminLoginView.as_view(),name='Admin-login-api-view'),
    path('admin/all-tutor/',AdminTutorView.as_view(),name='Admin-All-Tutor-api-view'),
    # path('admin/all-not-approved-tutor/',AdminNotApprovedTutorView.as_view(),name='admin-all-not-approved-tutor-api-view'),
    path('admin/all-not-approved-tutor/',AdminNotApprovedTutorApiView.as_view(),name='admin-all-not-approved-tutor-api-view'),
    path('admin/approve-tutor/<pk>',approveTutorByAdmin, name='admin-approve-tutor'),
    path('admin/all-approved-tutor/',AdminAllApprovedTutorView.as_view(), name='all-approved-tutor'),
    # path('admin/all-blocked-tutor/',getBlockedUserTutorApiView, name='all-blocked-ubblocked-api-view'),
    path('admin/all-blocked-tutor/',getBlockedTutorApiView.as_view(), name='all-blocked-ubblocked-api-view'),
    path('admin/blocked-unblocked-tutor/<pk>',AdminBlockedTutorOrUserView.as_view(), name='all-blocked-ubblocked-api-view'),
    path('admin/get-tutor-data/<pk>',TutorDataByIdApiView.as_view(), name='all-get-tutor-data-api-view'),
    path('admin/delete-user/<pk>',DeleteUserOrTutorApi.as_view(), name='all-get-tutor-data-api-view'),

    # admin user api
    path('admin/get-all-user/',AdminAllUserDataApiView.as_view(), name='all-get-tutor-data-api-view'),
    
    # Tutor Api
    path('tutor/register/',TutorRegisterApiView.as_view(),name='tutor-register-api-view'),
    path('tutor/login/',TutotLoginApiView.as_view(),name='tutor-login-api-view'),
    path('tutor/profile/',TutorProfifeAndUpdateApiView.as_view(),name='tutor-profile-api-view'),
    path('tutor/update/',TutorProfifeAndUpdateApiView.as_view(),name='tutor-update-api-view'),
    
] 