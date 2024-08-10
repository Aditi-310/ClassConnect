from django.contrib import admin
from django.urls import path,include
from rating.views import *

urlpatterns = [
    path('feedback-tutor/', UserFeedbackTutorApi.as_view(), name='feedbacck-tutor'),
    path('admin/tutor-feedback/', UserFeedbackRetrieveApi.as_view(), name='feedbacck-tutor'),
    path('admin/tutor-feedback/approve-disapprove/<pk>', FeedbackUpdateAndDeleteApi.as_view(), name='feedbacck-tutor'),
    path('admin/tutor-feedback/delete/<pk>', FeedbackUpdateAndDeleteApi.as_view(), name='feedbacck-tutor'),
    
    #tutor get feedback for his/her
    path('tutor/feedback/', TutorFeedbackGetApi.as_view(), name='feedbacck-tutor'),
    
    # api for showing comment/reviews in main page
    path('main/feedback/', MainPageRatingToShowApi.as_view(), name='main-page-api-view'),
    
    
    
]