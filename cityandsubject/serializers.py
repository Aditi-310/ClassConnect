from rest_framework import serializers
from api.models import City,Subject

# city serializer
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model=City
        fields='__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields = '__all__'