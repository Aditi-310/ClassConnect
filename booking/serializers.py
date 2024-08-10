from rest_framework import serializers
from api.models import User,Subject
from booking.models import Booking

# Order booking Api view
class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user_id.get_full_name",read_only=True)
    user_email = serializers.CharField(source='user_id.email',read_only=True)
    tutor_name = serializers.CharField(source="tutor_id.get_full_name",read_only=True)
    tutor_email = serializers.CharField(source="tutor_id.email",read_only=True)
    subject_name = serializers.CharField(source ='subject_id.subject_name',read_only=True)
    tutor_price = serializers.CharField(source="tutor_id.price",read_only=True)
    tutor_contact = serializers.CharField(source="tutor_id.contact",read_only=True)
    tutor_profile = serializers.CharField(source="tutor_id.profile_image",read_only=True)
    user_profile = serializers.CharField(source="user_id.profile_image",read_only=True)
    user_contact = serializers.CharField(source="user_id.contact",read_only=True)
    user_address = serializers.CharField(source="user_id.address",read_only=True)
    

    class Meta:
        model = Booking
        fields = '__all__'
        
        
class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'status',
            'cancellation_reason',
            'usr_cancellation_reason',
        ]
        
        
class BookingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            # 'id',
            'user_id',
            'tutor_id',
            'subject_id',
            'booking_time',
            'booking_date',
        ]