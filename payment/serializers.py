from rest_framework import serializers
from payment.models import Payment

class AdminPaymentSerializer(serializers.ModelSerializer):
    user_profile = serializers.CharField(source='user_id.profile_image',read_only=True)
    user_name = serializers.CharField(source='user_id.get_full_name',read_only=True)
    tutor_profile = serializers.CharField(source='tutor_id.profile_image',read_only=True)
    tutor_name = serializers.CharField(source='tutor_id.get_full_name',read_only=True)
    class Meta:
        model = Payment
        fields = [
            'id',
            'user_id',
            'tutor_id',
            'admin_amount',
            'tutor_amount',
            'payment_date',
            'user_profile',
            'tutor_profile',
            'user_name',
            'tutor_name',
        ]


class TutorPaymentSerializer(serializers.ModelSerializer):
    user_profile = serializers.CharField(source='user_id.profile_image',read_only=True)
    user_name = serializers.CharField(source='user_id.get_full_name',read_only=True)
    tutor_profile = serializers.CharField(source='tutor_id.profile_image',read_only=True)
    tutor_name = serializers.CharField(source='tutor_id.get_full_name',read_only=True)
    class Meta:
        model = Payment
        fields = [
            'id',
            'user_id',
            'tutor_id',
            'admin_amount',
            'tutor_amount',
            'payment_date',
            'user_profile',
            'tutor_profile',
            'user_name',
            'tutor_name',
        ]
        