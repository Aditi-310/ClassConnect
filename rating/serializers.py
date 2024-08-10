from rest_framework import serializers
from api.models import User,Subject
from rating.models import Feedback

#feed for tutor 
class TutorFeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        
class AdminSideFeedbackSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user_id.email",read_only=True)
    tutor_name = serializers.CharField(source="tutor_id.email",read_only=True)
    user_profile = serializers.ImageField(source='user_id.profile_image',read_only=True)
    tutor_profile = serializers.ImageField(source='tutor_id.profile_image',read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
        
class FeedbackForPerticularSeriliazer(serializers.ModelSerializer):
    user_email = serializers.CharField(source = 'user_id.email',read_only=True)
    user_name = serializers.CharField(source = 'user_id.get_full_name',read_only=True)
    user_profile = serializers.CharField(source = 'user_id.profile_image',read_only=True)
    user_contact = serializers.CharField(source = 'user_id.contact',read_only=True)
    class Meta:
        model = Feedback
        fields = [
            'tutor_id',
            'user_id',
            'review',
            'star',
            'user_email',
            'user_profile',
            'user_contact',
            'user_name'
        ]
        
class FeedbackSerializer(serializers.ModelSerializer):
    user_profile = serializers.ImageField(source='user_id.profile_image',read_only=True)
    user_name = serializers.CharField(source='user_id.get_full_name',read_only=True)
    class Meta:
        model = Feedback
        fields='__all__'